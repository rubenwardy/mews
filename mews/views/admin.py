from flask import render_template, redirect, url_for, send_file, abort, request, jsonify
from flask_user import login_required
from mews import app, lastfm
from mews.utils import scanForMusic, getArtistsInfo, getAlbumsInfo, importAllMusic
from mews.models import *


@app.route("/admin/")
@login_required
def admin():
	unknown_albums = Album.query.filter_by(is_known=False).order_by(Album.title).all()
	unknown_artists = Artist.query.filter_by(is_known=False).order_by(Artist.name).all()
	return render_template("admin/index.html", unknown_albums=unknown_albums, unknown_artists=unknown_artists,
			num_artists=Artist.query.count(), num_albums=Album.query.count(), num_tracks=Track.query.count())


@app.route("/admin/sync/albums/", methods=["POST"])
@login_required
def sync_album():
	getAlbumsInfo()
	return redirect(url_for("hello"))


@app.route("/admin/sync/artists/", methods=["POST"])
@login_required
def sync_artist():
	getArtistsInfo()
	return redirect(url_for("hello"))


@app.route("/admin/sync/music/", methods=["POST"])
@login_required
def sync_music():
	importAllMusic()
	return redirect(url_for("hello"))
