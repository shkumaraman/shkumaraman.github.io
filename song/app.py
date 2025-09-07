from flask import Flask, request, jsonify, send_file
from ytmusicapi import YTMusic
from flask_cors import CORS
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

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
def get_audio(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    mp4_file = f"{video_id}.mp4"
    mp3_file = f"{video_id}.mp3"

    # Download audio
    audio_stream.download(filename=mp4_file)

    # Convert to mp3
    clip = AudioFileClip(mp4_file)
    clip.write_audiofile(mp3_file)
    clip.close()
    os.remove(mp4_file)  # remove mp4

    # Serve mp3
    response = send_file(mp3_file, mimetype="audio/mpeg", as_attachment=False)

    # Delete mp3 after streaming
    @response.call_on_close
    def remove_file():
        os.remove(mp3_file)

    return response

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
