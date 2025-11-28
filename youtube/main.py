
from fastapi import FastAPI, HTTPException, Query
from youtubesearchpython import VideosSearch, ChannelsSearch, PlaylistsSearch, Video
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

app = FastAPI(
    title="Unofficial YouTube API",
    description="Simple unofficial wrapper around YouTube search, video details, and captions using youtubesearchpython + youtube-transcript-api.",
    version="2.0.0",
)


@app.get("/")
async def root():
    return {
        "name": "Unofficial YouTube API",
        "version": "2.0.0",
        "status": "ok",
        "docs": "/docs",
        "endpoints": {
            "video_search": "/search/videos?query=QUERY&limit=10",
            "channel_search": "/search/channels?query=QUERY&limit=10",
            "playlist_search": "/search/playlists?query=QUERY&limit=10",
            "video_details": "/video/{video_id}",
            "captions": "/captions/{video_id}?lang=en&format=json",
        },
    }


@app.get("/search/videos")
async def search_videos(
    query: str = Query(..., description="Search query for videos"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
):
    try:
        search = VideosSearch(query, limit=limit)
        return search.result()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/channels")
async def search_channels(
    query: str = Query(..., description="Search query for channels"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
):
    try:
        search = ChannelsSearch(query, limit=limit)
        return search.result()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/playlists")
async def search_playlists(
    query: str = Query(..., description="Search query for playlists"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
):
    try:
        search = PlaylistsSearch(query, limit=limit)
        return search.result()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/video/{video_id}")
async def get_video(video_id: str):
    """
    Get detailed information about a single video.
    video_id can be the full URL or the 11-character ID.
    """
    try:
        info = Video.getInfo(video_id)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _seconds_to_srt_timestamp(seconds: float) -> str:
    # Convert float seconds to SRT timestamp "HH:MM:SS,mmm"
    millis = int(round(seconds * 1000))
    hours = millis // (1000 * 60 * 60)
    millis %= 1000 * 60 * 60
    minutes = millis // (1000 * 60)
    millis %= 1000 * 60
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


@app.get("/captions/{video_id}")
async def get_captions(
    video_id: str,
    lang: str = Query("en", description="Preferred language code (e.g., en, hi, es)"),
    format: str = Query(
        "json",
        description="Response format: 'json' (default), 'text', or 'srt'",
        regex="^(json|text|srt)$",
    ),
):
    """
    Fetch YouTube video captions (subtitles) without official API key.

    - Tries to get manually uploaded subtitles in requested lang.
    - Falls back to auto-generated subtitles if needed.
    - Supports multiple output formats (json/text/srt).
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Choose transcript: try manual -> fallback to auto-generated in same lang
        try:
            transcript = transcript_list.find_transcript([lang])
        except Exception:
            # Try auto-generated transcript for that language
            try:
                transcript = transcript_list.find_generated_transcript([lang])
            except Exception:
                raise NoTranscriptFound

        data = transcript.fetch()

        # Collect available language codes
        available_languages = [t.language_code for t in transcript_list]

        if format == "text":
            text = "\n".join([item["text"] for item in data if item.get("text")])
            return {
                "video_id": video_id,
                "language": lang,
                "format": "text",
                "available_languages": available_languages,
                "captions_text": text,
            }

        if format == "srt":
            srt_lines = []
            for idx, c in enumerate(data, start=1):
                start = c.get("start", 0.0)
                duration = c.get("duration", 0.0)
                end = start + duration
                text = c.get("text", "").replace("\n", " ").strip()
                if not text:
                    continue
                srt_lines.append(str(idx))
                srt_lines.append(f"{_seconds_to_srt_timestamp(start)} --> {_seconds_to_srt_timestamp(end)}")
                srt_lines.append(text)
                srt_lines.append("")  # blank line
            srt_content = "\n".join(srt_lines)
            return {
                "video_id": video_id,
                "language": lang,
                "format": "srt",
                "available_languages": available_languages,
                "captions_srt": srt_content,
            }

        # Default: json
        return {
            "video_id": video_id,
            "language": lang,
            "format": "json",
            "available_languages": available_languages,
            "captions": data,
        }

    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No captions available for this video in the requested language.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
