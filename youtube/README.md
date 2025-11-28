
# Unofficial YouTube API (Python + FastAPI)

Simple unofficial wrapper around YouTube search, video details, and captions,
built with FastAPI and:
- [`youtubesearchpython`](https://pypi.org/project/youtubesearchpython/)
- [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/)

No official YouTube API key required.

## Endpoints

- `GET /` — health check and basic info

### Search
- `GET /search/videos?query=...&limit=10`
- `GET /search/channels?query=...&limit=10`
- `GET /search/playlists?query=...&limit=10`

### Video Details
- `GET /video/{video_id}` — details for a single video
  - `video_id` can be either the 11-char ID or the full YouTube URL.

### Captions (Subtitles)
- `GET /captions/{video_id}?lang=en&format=json`

Query params:
- `lang` — language code, e.g. `en`, `hi`, `es` (default: `en`)
- `format` — `json` (default), `text`, or `srt`

Examples:
- `GET /captions/dQw4w9WgXcQ?lang=en&format=json`
- `GET /captions/dQw4w9WgXcQ?lang=en&format=text`
- `GET /captions/dQw4w9WgXcQ?lang=en&format=srt`

Response (json format example):
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "format": "json",
  "available_languages": ["en", "hi"],
  "captions": [
    {"start": 0.0, "duration": 2.1, "text": "Intro..."},
    {"start": 2.1, "duration": 3.5, "text": "Hello everyone..."}
  ]
}
```

## Local run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open Swagger docs at: `http://127.0.0.1:8000/docs`

## Deploy on Render

1. Create a new **Web Service** on Render.
2. Connect this repo (or upload from the zip and push to a repo).
3. Use:

   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`

4. Deploy. After deployment you will get a base URL, for example:
   `https://your-service.onrender.com`

Then you can call:

```bash
curl "https://your-service.onrender.com/search/videos?query=lofi"
curl "https://your-service.onrender.com/captions/dQw4w9WgXcQ?lang=en&format=json"
```
