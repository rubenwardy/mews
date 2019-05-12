import os
from tinytag import TinyTag
import json
from . import lastfm
from .models import *
import pylast, json


ALLOWED_EXT = [".mp3", ".m4a", ".wav", ".ogg"]
def getMusicInfo(path):
	_, ext = os.path.splitext(path.lower())
	if ext in ALLOWED_EXT:
		return { "path": path, "meta": TinyTag.get(path) }
	else:
		return None


def scanForMusic(root):
	ret = []
	for dir, _, files in os.walk(root):
		for file in files:
			path = os.path.join(dir, file)
			info = getMusicInfo(path)
			if info is not None:
				ret.append(info)

	return ret


def getOrCreateArtist(artist):
	art = Artist.query.filter_by(name=artist).first()
	if art is None:
		art = Artist()
		art.name = artist
		db.session.add(art)

	return art


def getOrCreateAlbum(artist, title):
	art = getOrCreateArtist(artist)
	album = Album.query.filter_by(title=title, artist=art).first()
	if album is None:
		if art is None:
			art = Artist()
			art.name = artist
			db.session.add(art)

		album = Album()
		album.title = title
		album.artist = art
		db.session.add(album)

	return album


def getArtistsInfo():
	data = {}
	try:
		with open('artist_cache.json') as json_file:
			data = json.load(json_file)
	except FileNotFoundError:
		pass

	for artist in Artist.query.filter_by(is_known=False).all():
		try:
			key = artist.name.lower()
			if data.get(key):
				print("Using cached " + artist.name)
				artist.picture = data.get(key)["picture"]
				artist.is_known = artist.picture is not None
			else:
				print("Fetching " + artist.name)
				lfm_artist = lastfm.get_artist(artist.name)
				cname = lfm_artist.get_correction()
				if cname != artist.name:
					can = Artist.query.filter_by(name=cname).first()
					if can is None:
						print(" - corrected name to " + cname)
						artist.name = cname
					else:
						assert(can != artist)

						print(" - switching to canonical artist")
						Track.query.filter_by(artist_id=artist.id).update({ "artist_id": can.id })
						Album.query.filter_by(artist_id=artist.id).update({ "artist_id": can.id })
						db.session.delete(artist)
						artist = can

					lfm_artist = lastfm.get_artist(artist.name)


				if lfm_artist.get_mbid() is not None:
					# TODO: Artist picture support
					artist.is_known = True
				else:
					print(" - Artist not found: " + artist.name)

		except pylast.WSError:
			print(" - Error: " + artist.name)

	db.session.commit()

def getAlbumsInfo():
	data = {}
	try:
		with open('album_cache.json') as json_file:
			data = json.load(json_file)
	except FileNotFoundError:
		pass

	for album in Album.query.filter_by(is_known=False).all():
		try:
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


def importAllMusic():
	ret = scanForMusic(app.config["MUSIC_DIR"])

	Track.query.delete()
	Album.query.delete()
	Artist.query.delete()

	for info in ret:
		meta = info["meta"]

		if meta.title is not None:
			album = getOrCreateAlbum(artist=meta.albumartist or meta.artist, title=meta.album)
			artist = getOrCreateArtist(meta.artist)
			track = Track()
			track.album = album
			track.artist = artist
			track.title = meta.title
			track.path  = info["path"]
			db.session.add(track)

	db.session.commit()
