from flask import render_template, jsonify
from mew import app
from mew.models import *

@app.route("/api/albums/")
def api_albums():
	albums = db.session.query(Album).join(Artist.albums).order_by(Artist.name).all()
	return jsonify([ a.asDict() for a in albums ])
