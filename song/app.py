from flask import Flask, jsonify, request
from pytube import YouTube, Search

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Audio Backend Running!"

@app.route('/search')
def search_videos():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400
    s = Search(query)
    results = []
    for video in s.results[:10]:
        results.append({
            "video_id": video.video_id,
            "title": video.title,
            "thumbnail": video.thumbnail_url
        })
    return jsonify(results)

@app.route('/audio/<video_id>')
def get_audio(video_id):
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        return jsonify({
            "title": yt.title,
            "audio_url": audio_stream.url
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    
