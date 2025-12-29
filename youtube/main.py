from fastapi import FastAPI, HTTPException
import requests
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------------------
# 🛡 APP + CORS
# -------------------------------------------------------------
app = FastAPI(
    title="Unofficial YouTube API",
    description="YouTube Search + Video Details + Captions",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# 🏠 ROOT
# -------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "name": "YouTube API",
        "version": "1.0",
        "status": "ok",
        "docs": "/docs",
    }

# -------------------------------------------------------------
# 🔥 MOBILE SEARCH (STABLE)
# -------------------------------------------------------------
def youtube_search_mobile(query: str, limit: int = 10):
    url = f"https://m.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        html = requests.get(url, headers=headers, timeout=10).text
        raw_json = re.search(r"var ytInitialData = (.*?);</script>", html).group(1)
        data = json.loads(raw_json)
    except:
        return []

    results = []

    try:
        sections = data["contents"]["twoColumnSearchResultsRenderer"] \
            ["primaryContents"]["sectionListRenderer"]["contents"]
    except:
        return []

    for sec in sections:
        items = sec.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            video = item.get("videoRenderer")
            if not video:
                continue

            vid = video.get("videoId")
            title = video.get("title", {}).get("runs", [{}])[0].get("text")
            thumb = video.get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url")
            channel = video.get("ownerText", {}).get("runs", [{}])[0].get("text")
            duration = video.get("lengthText", {}).get("simpleText")
            views = video.get("viewCountText", {}).get("simpleText")

            results.append({
                "videoId": vid,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "thumbnail": thumb,
                "channel": channel,
                "views": views,
                "duration": duration,
            })

            if len(results) >= limit:
                return results

    return results

@app.get("/search/videos")
async def search_videos(query: str, limit: int = 10):
    return {
        "ok": True,
        "query": query,
        "results": youtube_search_mobile(query, limit)
    }

# -------------------------------------------------------------
# 🎯 VIDEO DETAILS
# -------------------------------------------------------------
@app.get("/video/{video_id}")
async def video_details(video_id: str):
    url = f"https://m.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        html = requests.get(url, headers=headers, timeout=10).text
        match = re.search(r'"title":"(.*?)"', html)
        title = match.group(1).encode("utf-8").decode("unicode_escape")
    except:
        title = "Unknown"

    return {
        "videoId": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }

# -------------------------------------------------------------
# 🕒 SRT TIME
# -------------------------------------------------------------
def _seconds_to_srt(seconds: float) -> str:
    ms = int(seconds * 1000)
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03d}"

# -------------------------------------------------------------
# 📝 CAPTIONS / LYRICS
# -------------------------------------------------------------
@app.get("/captions/{video_id}")
async def captions(video_id: str, lang: str = "en", format: str = "json"):
    try:
        data = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=[lang]
        )

        if format == "text":
            return {
                "video_id": video_id,
                "language": lang,
                "text": "\n".join(c["text"] for c in data)
            }

        if format == "srt":
            srt = []
            for i, c in enumerate(data, 1):
                start = c["start"]
                end = start + c["duration"]
                srt.append(str(i))
                srt.append(f"{_seconds_to_srt(start)} --> {_seconds_to_srt(end)}")
                srt.append(c["text"])
                srt.append("")
            return {"srt": "\n".join(srt)}

        return {
            "video_id": video_id,
            "language": lang,
            "captions": data
        }

    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No captions found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
