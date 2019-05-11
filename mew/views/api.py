from flask import render_template, jsonify
from mew import app

@app.route("/api/albums/")
def api_albums():
    albums = []
    return jsonify(albums)
