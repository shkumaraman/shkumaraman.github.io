import html as html_lib
import json
import re
import time
from contextlib import asynccontextmanager
from typing import Annotated, Any, Optional
from urllib.parse import quote_plus

import httpx
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cookie": "CONSENT=YES+1",
}

SEARCH_TTL = 300
VIDEO_TTL = 600
CACHE_MAX = 500


class TTLCache:
    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self.store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str):
        item = self.store.get(key)
        if not item:
            return None
        expires, value = item
        if expires < time.monotonic():
            self.store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, ttl: int):
        if len(self.store) >= self.maxsize:
            now = time.monotonic()
            for k in [k for k, (exp, _) in self.store.items() if exp < now]:
                self.store.pop(k, None)
            if len(self.store) >= self.maxsize:
                oldest = min(self.store, key=lambda k: self.store[k][0])
                self.store.pop(oldest, None)
        self.store[key] = (time.monotonic() + ttl, value)


cache = TTLCache(CACHE_MAX)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(
        headers=DEFAULT_HEADERS,
        timeout=12.0,
        follow_redirects=True,
    )
    yield
    await app.state.client.aclose()


app = FastAPI(
    title="Unofficial YouTube API",
    description="Fast, Non-blocking YouTube Search & Video Details Scraper",
    version="1.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_json(page: str, marker: str) -> Optional[dict]:
    for m in re.finditer(rf"{re.escape(marker)}\s*=\s*", page):
        try:
            obj, _ = json.JSONDecoder().raw_decode(page, m.end())
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def text_of(obj: Optional[dict]) -> Optional[str]:
    if not obj:
        return None
    if "simpleText" in obj:
        return obj["simpleText"]
    runs = obj.get("runs")
    if runs:
        return "".join(r.get("text", "") for r in runs)
    return None


def parse_youtube_search(page: str, limit: int = 10) -> list:
    data = extract_json(page, "ytInitialData")
    if not data:
        return []

    contents = data.get("contents", {})
    sections = (
        contents.get("twoColumnSearchResultsRenderer", {})
        .get("primaryContents", {})
        .get("sectionListRenderer", {})
        .get("contents")
        or contents.get("sectionListRenderer", {}).get("contents")
        or []
    )

    results = []

    for sec in sections:
        items = sec.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            video = item.get("videoRenderer")
            if not video:
                continue

            vid = video.get("videoId", "")
            if not vid:
                continue

            thumbs = video.get("thumbnail", {}).get("thumbnails", [])
            thumbnail = (
                thumbs[-1].get("url", "")
                if thumbs
                else f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            )

            channel_runs = video.get("ownerText", {}).get("runs", [])
            channel = channel_runs[0].get("text", "") if channel_runs else ""

            results.append(
                {
                    "videoId": vid,
                    "title": text_of(video.get("title")) or "",
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumbnail": thumbnail,
                    "channel": channel,
                    "views": text_of(video.get("viewCountText")),
                    "duration": text_of(video.get("lengthText")),
                    "publishedTime": text_of(video.get("publishedTimeText")),
                }
            )

            if len(results) >= limit:
                return results

    return results


async def fetch_page(url: str) -> str:
    client: httpx.AsyncClient = app.state.client
    try:
        resp = await client.get(url)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code if resp.status_code >= 400 else 502,
            detail="YouTube returned an error",
        )

    if "consent.youtube.com" in str(resp.url):
        raise HTTPException(
            status_code=502, detail="YouTube consent page blocked the request"
        )

    return resp.text


def og_value(page: str, prop: str) -> Optional[str]:
    m = re.search(
        rf'<meta\s+property="{re.escape(prop)}"\s+content="([^"]*)"', page
    )
    return html_lib.unescape(m.group(1)) if m else None


@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {
        "name": "Unofficial YouTube API",
        "version": "1.1",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/search/videos")
async def search_videos(
    query: Annotated[str, Query(min_length=1, description="Search keyword")],
    limit: Annotated[int, Query(ge=1, le=20, description="Max results (1 to 20)")] = 10,
):
    cache_key = f"search:{query.strip().lower()}"
    cached = cache.get(cache_key)

    if cached is None:
        url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        page = await fetch_page(url)
        cached = parse_youtube_search(page, limit=20)
        if cached:
            cache.set(cache_key, cached, SEARCH_TTL)

    data = cached[:limit]
    return {
        "ok": True,
        "query": query,
        "count": len(data),
        "results": data,
    }


@app.get("/video/{video_id}")
async def video_details(
    video_id: Annotated[str, Path(description="11 character YouTube video ID")],
):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{11}", video_id):
        raise HTTPException(
            status_code=400, detail="Invalid YouTube Video ID format"
        )

    cache_key = f"video:{video_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"https://www.youtube.com/watch?v={video_id}"
    page = await fetch_page(url)

    player_data = extract_json(page, "ytInitialPlayerResponse")

    if player_data:
        playability = player_data.get("playabilityStatus", {})
        status = playability.get("status")
        if status and status != "OK":
            reason = playability.get("reason") or status
            raise HTTPException(
                status_code=404, detail=f"Video unavailable: {reason}"
            )

        details = player_data.get("videoDetails")
        if details:
            thumbs = details.get("thumbnail", {}).get("thumbnails", [])
            thumbnail_url = (
                thumbs[-1].get("url")
                if thumbs
                else f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            )

            length = details.get("lengthSeconds")
            result = {
                "ok": True,
                "videoId": video_id,
                "title": details.get("title"),
                "channel": details.get("author"),
                "channelId": details.get("channelId"),
                "durationSeconds": int(length) if length and length.isdigit() else None,
                "views": details.get("viewCount"),
                "isLive": bool(details.get("isLive", False)),
                "wasLive": bool(details.get("isLiveContent", False)),
                "description": details.get("shortDescription", ""),
                "thumbnail": thumbnail_url,
                "url": url,
            }
            cache.set(cache_key, result, VIDEO_TTL)
            return result

    title = og_value(page, "og:title")
    if not title:
        raise HTTPException(
            status_code=404, detail="Video not found or page could not be parsed"
        )

    result = {
        "ok": True,
        "videoId": video_id,
        "title": title,
        "channel": None,
        "channelId": None,
        "durationSeconds": None,
        "views": None,
        "isLive": False,
        "wasLive": False,
        "description": og_value(page, "og:description") or "",
        "thumbnail": og_value(page, "og:image")
        or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "url": url,
    }
    cache.set(cache_key, result, VIDEO_TTL)
    return result
