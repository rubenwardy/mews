from flask import render_template, redirect, url_for, send_file
from mews import app, lastfm
from mews.utils import scanForMusic
from mews.models import *
import pylast, json

@app.route("/")
def hello():
	return render_template("home.html")


@app.route("/tracks/<int:id>/")
def track_file(id):
	track = Track.query.get(id)
	if track is None:
		print("No track!")
		abort(404)

	print(track.path)
	return send_file(track.path)


@app.route("/sync/albums/")
def sync_album():
	data = {}
	with open('album_cache.json') as json_file:
		data = json.load(json_file)

	for album in Album.query.all():
		try:
			if album.is_known:
				continue

			key = (album.artist.name + "/" + album.title).lower()
			if data.get(key):
				print("Using cached " + album.title + " by " + album.artist.name)
				album.picture = data.get(key)["picture"]
				album.is_known = album.picture is not None
			else:
				print("Fetching " + album.title + " by " + album.artist.name)
				lfm_album = lastfm.get_album(album.artist.name, album.title)
				album.title = lfm_album.get_title()
				album.picture = lfm_album.get_cover_image()
				album.is_known = True
			db.session.commit()
		except pylast.WSError:
			print("Error")

	return redirect(url_for("hello"))


@app.route("/sync/")
def sync():
	ret = scanForMusic(app.config["MUSIC_DIR"])

	Track.query.delete()
	Album.query.delete()
	Artist.query.delete()

	for info in ret:
		meta = info["meta"]

		if meta.title is not None:
			album = getOrCreateAlbum(artist=meta.albumartist or meta.artist, title=meta.album)

			track = Track()
			track.album = album
			track.title = meta.title
			track.path  = info["path"]
			db.session.add(track)

		# tag.album         # album as string
		# tag.albumartist   # album artist as string
		# tag.artist        # artist name as string
		# tag.audio_offset  # number of bytes before audio data begins
		# tag.bitrate       # bitrate in kBits/s
		# tag.comment       # file comment as string
		# tag.composer      # composer as string
		# tag.disc          # disc number
		# tag.disc_total    # the total number of discs
		# tag.duration      # duration of the song in seconds
		# tag.filesize      # file size in bytes
		# tag.genre         # genre as string
		# tag.samplerate    # samples per second
		# tag.title         # title of the song
		# tag.track         # track number as string
		# tag.track_total   # total number of tracks as string
		# tag.year          # year or data as string

	db.session.commit()
	return redirect(url_for("hello"))

from . import sass, api, dummyart
