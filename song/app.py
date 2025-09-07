from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://www.jiosaavn.com/api.php"


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
    r = requests.get(BASE_URL, params=params)
    return jsonify(r.json())


@app.route("/song/")
def song_details():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide song id or link"}), 400

    params = {
        "__call": "song.getDetails",
        "pids": query.split("/")[-1],  # Extract ID if link provided
        "_format": "json",
        "_marker": "0"
    }
    r = requests.get(BASE_URL, params=params)
    return jsonify(r.json())


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
    r = requests.get(BASE_URL, params=params)
    return jsonify(r.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
