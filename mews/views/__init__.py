from flask import render_template, redirect, url_for, send_file
from mews import app
from mews.utils import scanForMusic
from mews.models import *

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


@app.route("/sync/")
def sync():
	ret = scanForMusic(app.config["MUSIC_DIR"])

	Track.query.delete()
	Album.query.delete()
	Artist.query.delete()

	for info in ret:
		meta = info["meta"]
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
