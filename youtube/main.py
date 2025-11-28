from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import requests
from bs4 import BeautifulSoup
import json
import re

app = FastAPI(
    title="Unofficial YouTube API (Stable Version)",
    description="YouTube search, video details & captions without any unstable libraries.",
    version="3.0.0",
)


@app.get("/")
async def root():
    return {
        "name": "Unofficial YouTube API",
        "version": "3.0.0",
        "status": "ok",
        "docs": "/docs",
        "endpoints": {
            "video_search": "/search/videos?query=QUERY&limit=10",
            "video_details": "/video/VIDEO_ID",
            "captions": "/captions/VIDEO_ID",
        },
    }


# ----------------------------------------------------
#  SIMPLE YOUTUBE SEARCH (NO API KEY, NO BROKEN LIBS)
# ----------------------------------------------------
def youtube_search(query: str, limit: int = 10):
    url = "https://www.youtube.com/results"
    params = {"search_query": query}

    response = requests.get(url, params=params)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")

    data = None
    for script in scripts:
        if "ytInitialData" in script.text:
            try:
                text = script.text
                json_str = text.split("ytInitialData = ")[1].split(";</script>")[0]
                data = json.loads(json_str)
                break
            except:
                continue

    if not data:
        return []

    results = []
    try:
        sections = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
    except:
        return []

    for sec in sections:
        items = sec.get("itemSectionRenderer", {}).get("contents", [])
        for item in items:
            if "videoRenderer" in item:
                v = item["videoRenderer"]
                video_id = v["videoId"]
                title = v["title"]["runs"][0]["text"]
                thumbnail = v["thumbnail"]["thumbnails"][-1]["url"]
                channel = v["ownerText"]["runs"][0]["text"] if "ownerText" in v else None
                duration = v["lengthText"]["simpleText"] if "lengthText" in v else None
                views = v["viewCountText"]["simpleText"] if "viewCountText" in v else None

                results.append({
                    "videoId": video_id,
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
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
    query: str = Query(..., description="Search query for YouTube videos"),
    limit: int = Query(10, ge=1, le=50)
):
    try:
        data = youtube_search(query, limit)
        return {"results": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------------------------------
#       SIMPLE VIDEO DETAILS (TITLE SCRAPER)
# ----------------------------------------------------
@app.get("/video/{video_id}")
async def video_details(video_id: str):
    url = f"https://www.youtube.com/watch?v={video_id}"
    response = requests.get(url)

    # Title extraction from HTML
    match = re.search(r'"title":"(.*?)"', response.text)
    title = match.group(1).encode("utf-8").decode("unicode_escape") if match else "Unknown"

    return {
        "videoId": video_id,
        "title": title,
        "url": url
    }


# ----------------------------------------------------
#                CAPTIONS (TRANSCRIPTS)
# ----------------------------------------------------
def _seconds_to_srt_timestamp(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours = millis // (1000 * 60 * 60)
    millis %= 1000 * 60 * 60
    minutes = millis // (1000 * 60)
    millis %= 1000 * 60
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


@app.get("/captions/{video_id}")
async def captions(
    video_id: str,
    lang: str = "en",
    format: str = "json"
):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # manual or auto
        try:
            transcript = transcript_list.find_transcript([lang])
        except:
            transcript = transcript_list.find_generated_transcript([lang])

        data = transcript.fetch()

        available = [t.language_code for t in transcript_list]

        # plain text
        if format == "text":
            text = "\n".join([x["text"] for x in data])
            return {"video_id": video_id, "language": lang, "captions": text}

        # SRT format
        if format == "srt":
            srt = []
            for i, c in enumerate(data, 1):
                start = c["start"]
                end = start + c["duration"]
                srt.append(str(i))
                srt.append(f"{_seconds_to_srt_timestamp(start)} --> {_seconds_to_srt_timestamp(end)}")
                srt.append(c["text"])
                srt.append("")
            return {"video_id": video_id, "language": lang, "captions_srt": "\n".join(srt)}

        # JSON
        return {
            "video_id": video_id,
            "language": lang,
            "available_languages": available,
            "captions": data
        }

    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No captions for this video.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
