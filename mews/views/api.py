from flask import render_template, jsonify, request, abort
from flask_user import login_required
from mews import app
from mews.models import *

@app.route("/api/tracks/<int:id>/")
def api_track(id):
	track = Track.query.get(id)
	if track is None:
		abort(404)

	return jsonify(track.asDict())


@app.route("/api/albums/")
def api_albums():
	albums = db.session.query(Album).join(Artist.albums).order_by(Artist.name).all()
	return jsonify([ a.asDict() for a in albums ])


@app.route("/api/albums/<int:id>/tracks/")
def api_album_tracks(id):
	album = Album.query.get(id)
	if album is None:
		abort(404)

	return jsonify([ t.asDict(t.id) for t in album.tracks ])


@app.route("/api/album_cache/")
@login_required
def api_album_cache():
	ret = {}

	albums = db.session.query(Album).join(Artist.albums).filter_by(is_known=True).all()
	for album in albums:
		ret[(album.artist.name + "/" + album.title).lower()] = album.asDict(add_id=False)

	return jsonify(ret)


@app.route("/api/artist_cache/")
@login_required
def api_artist_cache():
	ret = {}

	artists = Artist.query.filter_by(is_known=True).all()
	for artist in artists:
		ret[artist.name.lower()] = artist.asDict(add_id=False)

	return jsonify(ret)


@app.route("/api/playlists/")
@login_required
def api_playlists():
	playlists = Playlist.query.all()
	return jsonify([ p.asDict() for p in playlists ])


@app.route("/api/playlists/new/", methods=["POST"])
@login_required
def api_playlist_create():
	playlist = Playlist()
	playlist.title = request.form.get("title") or "Untitled Playlist"
	db.session.add(playlist)
	db.session.commit()
	return jsonify(playlist.asDict())


@app.route("/api/playlists/<int:id>/tracks/", methods=["GET", "POST"])
@login_required
def api_playlist_tracks(id):
	playlist = Playlist.query.get(id)
	if playlist is None:
		abort(404)

	if request.method == "POST":
		to_add = request.get_json()

		insert_at = len(playlist.tracks)

		if "after" in to_add:
			pt = PlaylistTrack.query.get(int(to_add["after"]))
			if pt is None:
				abort(400)

			insert_at = pt.position + 1

		if "clear" in to_add:
			playlist.tracks = []

		if "albums" in to_add:
			for album_id in to_add["albums"]:
				album = Album.query.get(album_id)
				if album is None:
					continue

				playlist.tracks.extend(album.tracks)

		if "tracks" in to_add:
			tracks = to_add["tracks"]

			for track_id in tracks:
				track = Track.query.get(track_id)
				if track is None:
					continue

				playlist.tracks.insert(insert_at, track)
				insert_at += 1


	db.session.commit()

	return jsonify([ t.track.asDict(t.id) for t in playlist._tracks ])
