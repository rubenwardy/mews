from flask import render_template, redirect, url_for, send_file
from flask_user import login_required
from mews import app, lastfm
from mews.utils import scanForMusic, getArtistsInfo, getAlbumsInfo, importAllMusic
from mews.models import *

@app.route("/")
def hello():
	return render_template("home.html")


@app.route("/problems/")
@login_required
def problems():
	unknown_albums = Album.query.filter_by(is_known=False).order_by(Album.title).all()
	unknown_artists = Artist.query.filter_by(is_known=False).order_by(Artist.name).all()
	return render_template("problems.html", unknown_albums=unknown_albums, unknown_artists=unknown_artists)


@app.route("/tracks/<int:id>/")
@login_required
def track_file(id):
	track = Track.query.get(id)
	if track is None:
		print("No track!")
		abort(404)

	print(track.path)
	return send_file(track.path)


@app.route("/sync/albums/")
@login_required
def sync_album():
	getAlbumsInfo()
	return redirect(url_for("hello"))


@app.route("/sync/artists/")
@login_required
def sync_artist():
	getArtistsInfo()
	return redirect(url_for("hello"))


@app.route("/sync/")
@login_required
def sync():
	importAllMusic()
	return redirect(url_for("hello"))

from . import sass, api, dummyart
