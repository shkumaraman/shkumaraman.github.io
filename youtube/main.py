from fastapi import FastAPI, HTTPException, Query
import requests
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import yt_dlp

# -------------------------------------------------------------
# 🛡 CORS ENABLED
# -------------------------------------------------------------
app = FastAPI(
    title="Unofficial YouTube API (Stable V8)",
    description="YouTube Search + Details + Captions + Audio Stream",
    version="8.0.0",
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
        "version": "8.0.0",
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
                duration_obj.get("simpleText") or
                (duration_obj.get("runs", [{}])[0].get("text") if "runs" in duration_obj else None)
            )
            view_obj = video.get("viewCountText", {})
            views = (
                view_obj.get("simpleText") or
                (view_obj.get("runs", [{}])[0].get("text") if "runs" in view_obj else None)
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


# -------------------------------------------------------------
# 🎵 STREAM AUDIO (MAIN FEATURE)
# -------------------------------------------------------------
@app.get("/stream/{video_id}")
async def stream_audio(video_id: str):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            stream_url = info["url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract stream: {str(e)}")

    def audio_generator():
        try:
            audio = requests.get(stream_url, stream=True)
            for chunk in audio.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
        except:
            return

    return StreamingResponse(audio_generator(), media_type="audio/mp4")


# -------------------------------------------------------------
# 📝 CAPTIONS
# -------------------------------------------------------------
def _seconds_to_srt_timestamp(seconds: float) -> str:
    millis = int(seconds * 1000)
    hours = millis // 3600000
    millis %= 3600000
    minutes = millis // 60000
    millis %= 60000
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


@app.get("/captions/{video_id}")
async def captions(video_id: str, lang: str = "en", format: str = "json"):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            t = transcripts.find_transcript([lang])
        except:
            t = transcripts.find_generated_transcript([lang])

        data = t.fetch()
        available = [x.language_code for x in transcripts]

        if format == "text":
            return {"text": "\n".join([c["text"] for c in data])}

        if format == "srt":
            srt = []
            for i, c in enumerate(data, 1):
                start = c["start"]
                end = start + c["duration"]
                srt.append(str(i))
                srt.append(f"{_seconds_to_srt_timestamp(start)} --> {_seconds_to_srt_timestamp(end)}")
                srt.append(c["text"])
                srt.append("")
            return {"srt": "\n".join(srt)}

        return {
            "video_id": video_id,
            "language": lang,
            "available_languages": available,
            "captions": data,
        }

    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No captions found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
