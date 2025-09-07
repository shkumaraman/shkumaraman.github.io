from flask import Flask, request, jsonify, Response
from ytmusicapi import YTMusic
from flask_cors import CORS
from pytube import YouTube

app = Flask(__name__)
CORS(app)

ytmusic = YTMusic()

@app.route('/')
def home():
    return {"message": "YouTube Music API running on Render!"}

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter ?q="}), 400
    
    results = ytmusic.search(query, filter="songs")
    songs = []
    for song in results[:10]:
        songs.append({
            "title": song['title'],
            "artist": song['artists'][0]['name'] if song['artists'] else "Unknown",
            "videoId": song['videoId'],
            "audioUrl": f"/audio/{song['videoId']}"
        })
    return jsonify(songs)

@app.route('/audio/<video_id>')
def stream_audio(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    # Stream chunks to browser
    def generate():
        buffer = audio_stream.stream_to_buffer()
        while True:
            chunk = buffer.read(1024*32)
            if not chunk:
                break
            yield chunk
    
    return Response(generate(), mimetype="audio/mp4")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
