from fastapi import FastAPI, HTTPException
import requests
import re
import json
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------------------
# 🛡 CORS ENABLED
# -------------------------------------------------------------
app = FastAPI(
    title="Unofficial YouTube API",
    description="YouTube Search + Details",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "YouTube API",
        "version": "1.0",
        "status": "ok",
        "docs": "/docs",
    }


# -------------------------------------------------------------
# 🔥 SUPER STABLE MOBILE SEARCH
# -------------------------------------------------------------
def youtube_search_mobile(query: str, limit: int = 10):
    url = f"https://m.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        html = requests.get(url, headers=headers, timeout=10).text
    except:
        return []

    try:
        raw_json = re.search(r"var ytInitialData = (.*?);</script>", html).group(1)
        data = json.loads(raw_json)
    except:
        return []

    results = []

    try:
        main = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]
        sections = main["sectionListRenderer"]["contents"]
    except:
        return []

    for sec in sections:
        items = sec.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            video = item.get("videoRenderer")
            if not video:
                continue

            vid = video.get("videoId", "")
            title = video.get("title", {}).get("runs", [{}])[0].get("text", "")
            thumbnail = video.get("thumbnail", {}).get("thumbnails", [{}])[-1].get("url", "")
            channel = video.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
            duration_obj = video.get("lengthText", {})
            duration = (
                duration_obj.get("simpleText")
                or (duration_obj.get("runs", [{}])[0].get("text") if "runs" in duration_obj else None)
            )
            view_obj = video.get("viewCountText", {})
            views = (
                view_obj.get("simpleText")
                or (view_obj.get("runs", [{}])[0].get("text") if "runs" in view_obj else None)
            )

            results.append({
                "videoId": vid,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "thumbnail": thumbnail,
                "channel": channel,
                "views": views,
                "duration": duration,
            })

            if len(results) >= limit:
                return results

    return results


@app.get("/search/videos")
async def search_videos(query: str, limit: int = 10):
    try:
        data = youtube_search_mobile(query, limit)
        return {"ok": True, "query": query, "count": len(data), "results": data}
    except Exception as e:
        return {"ok": False, "error": str(e), "results": []}


# -------------------------------------------------------------
# 🎯 VIDEO DETAILS
# -------------------------------------------------------------
@app.get("/video/{video_id}")
async def video_details(video_id: str):
    url = f"https://m.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        html = requests.get(url, headers=headers, timeout=10).text
    except:
        raise HTTPException(status_code=500, detail="Failed to connect")

    match = re.search(r'"title":"(.*?)"', html)
    title = match.group(1).encode("utf-8").decode("unicode_escape") if match else "Unknown"

    return {
        "videoId": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }
