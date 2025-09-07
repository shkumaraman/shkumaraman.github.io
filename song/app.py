from flask import Flask, request, jsonify
from ytmusicapi import YTMusic
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
            "videoId": song['videoId']
        })
    return jsonify(songs)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    
