from flask import render_template, jsonify
from mew import app

@app.route("/api/albums/")
def api_albums():
    albums = [ { "id":"muse-st", "artist": "Muse", "title": "Simulation Theory", "album": "https://i.redd.it/337x5bx7x7j11.jpg" } ]
    return jsonify(albums)
