from flask import Flask, Response
import threading
import selenium_session as session
import time

app = Flask(__name__)

# Start keep-alive thread
threading.Thread(target=session.keep_alive, daemon=True).start()

@app.route("/")
def home():
    html = session.get_page_source()
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
