import json
import re
from contextlib import asynccontextmanager
from urllib.parse import quote_plus

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

# -------------------------------------------------------------
# 🌐 LIFESPAN & HTTP CLIENT (Reusable Connection Pool)
# -------------------------------------------------------------
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # App start hone par HTTP client initialize hoga
    app.state.client = httpx.AsyncClient(
        headers=DEFAULT_HEADERS,
        timeout=12.0,
        follow_redirects=True,
    )
    yield
    # App band hone par connection cleanly close hoga
    await app.state.client.aclose()


# -------------------------------------------------------------
# 🚀 FASTAPI APP SETUP
# -------------------------------------------------------------
app = FastAPI(
    title="Unofficial YouTube API",
    description="Fast, Non-blocking YouTube Search & Video Details Scraper",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# 🔍 SEARCH PARSER HELPER
# -------------------------------------------------------------
def parse_youtube_search(html: str, limit: int = 10) -> list:
    # ytInitialData extract karne ke multiple regex patterns
    match = re.search(
        r"var\s+ytInitialData\s*=\s*({.+?});\s*<\/script>", html
    ) or re.search(r"ytInitialData\s*=\s*({.+?});", html)

    if not match:
        return []

    try:
        data = json.loads(match.group(1))
    except Exception:
        return []

    # Section List dhoondna (Desktop aur Mobile dono cover karta hai)
    sections = []
    try:
        sections = data["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"]
    except KeyError:
        try:
            sections = data["contents"]["sectionListRenderer"]["contents"]
        except KeyError:
            return []

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

            # Title
            title = ""
            if "title" in video and "runs" in video["title"]:
                title = "".join(
                    r.get("text", "") for r in video["title"]["runs"]
                )
            elif "title" in video and "simpleText" in video["title"]:
                title = video["title"]["simpleText"]

            # Thumbnail
            thumbs = video.get("thumbnail", {}).get("thumbnails", [])
            thumbnail = (
                thumbs[-1].get("url", "")
                if thumbs
                else f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            )

            # Channel / Author
            channel_runs = video.get("ownerText", {}).get("runs", [])
            channel = channel_runs[0].get("text", "") if channel_runs else ""

            # Duration
            duration_obj = video.get("lengthText", {})
            duration = duration_obj.get("simpleText") or (
                duration_obj.get("runs", [{}])[0].get("text")
                if "runs" in duration_obj
                else None
            )

            # Views
            view_obj = video.get("viewCountText", {})
            views = view_obj.get("simpleText") or (
                view_obj.get("runs", [{}])[0].get("text")
                if "runs" in view_obj
                else None
            )

            # Published Time (e.g., "2 days ago")
            published_time = video.get("publishedTimeText", {}).get(
                "simpleText"
            )

            results.append(
                {
                    "videoId": vid,
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumbnail": thumbnail,
                    "channel": channel,
                    "views": views,
                    "duration": duration,
                    "publishedTime": published_time,
                }
            )

            if len(results) >= limit:
                return results

    return results


# -------------------------------------------------------------
# 📌 ROUTES
# -------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "name": "Unofficial YouTube API",
        "version": "2.0",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/search/videos")
async def search_videos(
    query: str = Query(..., description="Search keyword"),
    limit: int = Query(10, ge=1, le=50, description="Max results (1 to 50)"),
):
    encoded_query = quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    try:
        client: httpx.AsyncClient = app.state.client
        resp = await client.get(url)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail="YouTube returned an error",
            )

        data = parse_youtube_search(resp.text, limit=limit)
        return {
            "ok": True,
            "query": query,
            "count": len(data),
            "results": data,
        }
    except HTTPException:
        raise
    except Exception as e:
        return {"ok": False, "error": str(e), "results": []}


@app.get("/video/{video_id}")
async def video_details(video_id: str):
    # Clean ID validation (YouTube IDs are typically 11 alphanumeric chars)
    if not re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
        raise HTTPException(
            status_code=400, detail="Invalid YouTube Video ID format"
        )

    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        client: httpx.AsyncClient = app.state.client
        resp = await client.get(url)
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail="Failed to load YouTube watch page",
            )

        html = resp.text

        # 1. Primary: ytInitialPlayerResponse extract karna
        player_match = re.search(
            r"ytInitialPlayerResponse\s*=\s*({.+?});", html
        )
        if player_match:
            try:
                player_data = json.loads(player_match.group(1))
                details = player_data.get("videoDetails", {})
                thumbs = details.get("thumbnail", {}).get("thumbnails", [])
                thumbnail_url = (
                    thumbs[-1].get("url")
                    if thumbs
                    else f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                )

                return {
                    "ok": True,
                    "videoId": video_id,
                    "title": details.get("title"),
                    "channel": details.get("author"),
                    "channelId": details.get("channelId"),
                    "durationSeconds": int(details.get("lengthSeconds", 0))
                    if details.get("lengthSeconds")
                    else None,
                    "views": details.get("viewCount"),
                    "isLive": details.get("isLiveContent", False),
                    "description": details.get("shortDescription", ""),
                    "thumbnail": thumbnail_url,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                }
            except Exception:
                pass

        # 2. Fallback: Agar player data na mile toh OpenGraph Meta Tags se fetch karein
        og_title = re.search(
            r'<meta\s+property="og:title"\s+content="([^"]*)"', html
        )
        og_image = re.search(
            r'<meta\s+property="og:image"\s+content="([^"]*)"', html
        )
        og_desc = re.search(
            r'<meta\s+property="og:description"\s+content="([^"]*)"', html
        )

        title = og_title.group(1) if og_title else "Unknown"

        return {
            "ok": True,
            "videoId": video_id,
            "title": title,
            "channel": None,
            "views": None,
            "durationSeconds": None,
            "isLive": False,
            "description": og_desc.group(1) if og_desc else "",
            "thumbnail": og_image.group(1)
            if og_image
            else f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )
