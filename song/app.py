from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow all cross-origin requests

BASE_URL = "https://www.jiosaavn.com/api.php"

def call_api(params):
    try:
        r = requests.get(BASE_URL, params=params)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def home():
    return jsonify({"message": "JioSaavn API is running"})


@app.route("/result/")
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide query param"}), 400
    params = {
        "__call": "autocomplete.get",
        "query": query,
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/song/")
def song_details():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide song id or link"}), 400
    song_id = query.split("/")[-1]
    params = {
        "__call": "song.getDetails",
        "pids": song_id,
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/lyrics/")
def lyrics():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide song id"}), 400
    params = {
        "__call": "lyrics.getLyrics",
        "lyrics_id": query,
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/album/")
def album_details():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide album id or link"}), 400
    album_id = query.split("/")[-1]
    params = {
        "__call": "album.getAlbumDetails",
        "albumid": album_id,
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/playlist/")
def playlist_details():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide playlist id or link"}), 400
    playlist_id = query.split("/")[-1]
    params = {
        "__call": "playlist.getDetails",
        "playlistid": playlist_id,
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/artist/")
def artist_details():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide artist id or link"}), 400
    artist_id = query.split("/")[-1]
    params = {
        "__call": "artist.getArtistDetails",
        "artistid": artist_id,
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/topcharts/")
def top_charts():
    params = {
        "__call": "charts.getCharts",
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


@app.route("/newreleases/")
def new_releases():
    params = {
        "__call": "newreleases.get",
        "_format": "json",
        "_marker": "0"
    }
    return jsonify(call_api(params))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
