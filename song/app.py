from flask import Flask, request, jsonify, send_file
from ytmusicapi import YTMusic
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app)  # Allow frontend requests

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
    for song in results[:10]:  # Top 10 songs
        songs.append({
            "title": song['title'],
            "artist": song['artists'][0]['name'] if song['artists'] else "Unknown",
            "videoId": song['videoId'],
            "audioUrl": f"/audio/{song['videoId']}"  # frontend use karega
        })
    return jsonify(songs)

@app.route('/audio/<video_id>')
def get_audio(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    file_path = f"{video_id}.mp4"
    audio_stream.download(filename=file_path)
    
    # Serve audio for <audio> tag
    response = send_file(file_path, mimetype="audio/mp4", as_attachment=False)
    
    # Delete file after streaming complete
    @response.call_on_close
    def remove_file():
        os.remove(file_path)
    
    return response

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
