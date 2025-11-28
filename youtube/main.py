from fastapi import FastAPI, HTTPException, Query
import requests
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

app = FastAPI(
    title="Unofficial YouTube API (Ultimate Version)",
    description="YouTube search, video details & captions using m.youtube.com parser. 100% Render compatible.",
    version="4.0.0",
)


@app.get("/")
async def root():
    return {
        "name": "YouTube API",
        "version": "4.0.0",
        "status": "ok",
        "docs": "/docs",
        "endpoints": {
            "search": "/search/videos?query=QUERY&limit=10",
            "details": "/video/{video_id}",
            "captions": "/captions/{video_id}",
        },
    }


# ----------------------------------------------------
#   🔥 YOUTUBE SEARCH (MOBILE VERSION SCRAPER)
#   100% WORKING ON RENDER / NO JS REQUIRED
# ----------------------------------------------------
def youtube_search_mobile(query: str, limit: int = 10):
    url = f"https://m.youtube.com/results?search_query={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    html = requests.get(url, headers=headers).text

    # Extract ytInitialData
    try:
        data_json = re.search(r"var ytInitialData = (.*?);</script>", html).group(1)
        data = json.loads(data_json)
    except:
        return []

    results = []

    try:
        contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    except:
        return results

    for sec in contents:
        items = sec.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            video = item.get("videoRenderer")
            if video:
                vid = video["videoId"]
                title = video["title"]["runs"][0]["text"]
                thumbnail = video["thumbnail"]["thumbnails"][-1]["url"]
                channel = video["ownerText"]["runs"][0]["text"] if "ownerText" in video else None
                views = video["viewCountText"]["simpleText"] if "viewCountText" in video else None
                duration = video["lengthText"]["simpleText"] if "lengthText" in video else None

                results.append({
                    "videoId": vid,
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumbnail": thumbnail,
                    "channel": channel,
                    "views": views,
                    "duration": duration
                })

                if len(results) >= limit:
                    return results

    return results


@app.get("/search/videos")
async def search_videos(
    query: str = Query(...),
    limit: int = Query(10, ge=1, le=50)
):
    try:
        data = youtube_search_mobile(query, limit)
        return {"query": query, "count": len(data), "results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
#        🎯 VIDEO DETAILS (TITLE SCRAPER)
# ----------------------------------------------------
@app.get("/video/{video_id}")
async def video_details(video_id: str):
    url = f"https://m.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    html = requests.get(url, headers=headers).text

    # extract title
    title_match = re.search(r'"title":"(.*?)"', html)
    title = title_match.group(1).encode("utf-8").decode("unicode_escape") if title_match else "Unknown"

    return {
        "videoId": video_id,
        "title": title,
        "url": f"https://www.youtube.com/watch?v={video_id}"
    }


# ----------------------------------------------------
#          📝 CAPTIONS (TRANSCRIPTS)
# ----------------------------------------------------
def _seconds_to_srt_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
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
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # manual or auto
        try:
            transcript = transcript_list.find_transcript([lang])
        except:
            transcript = transcript_list.find_generated_transcript([lang])

        data = transcript.fetch()
        available = [t.language_code for t in transcript_list]

        if format == "text":
            return {"captions": "\n".join([x["text"] for x in data])}

        if format == "srt":
            srt = []
            for i, c in enumerate(data, 1):
                start = c["start"]
                end = start + c["duration"]
                srt.append(str(i))
                srt.append(f"{_seconds_to_srt_timestamp(start)} --> {_seconds_to_srt_timestamp(end)}")
                srt.append(c["text"])
                srt.append("")
            return {"captions_srt": "\n".join(srt)}

        return {
            "video_id": video_id,
            "language": lang,
            "captions": data,
            "available_languages": available
        }

    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No captions available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
