import os, random, string, imghdr
from tinytag import TinyTag
import json
from . import lastfm
from .models import *
from sqlalchemy import or_
import pylast, json


def randomString(n):
	return ''.join(random.choice(string.ascii_lowercase + \
		string.ascii_uppercase + string.digits) for _ in range(n))


ALLOWED_IMAGES = { "jpeg": True, "png": True, "gif": True, "bmp": True }
def getImageType(data):
	ext = imghdr.what(None, data)
	if ext in ALLOWED_IMAGES:
		return ext
	else:
		return None


ALLOWED_EXT = [".mp3", ".m4a", ".wav", ".ogg"]
def getMusicInfo(path):
	_, ext = os.path.splitext(path.lower())
	if ext in ALLOWED_EXT:
		return { "path": path, "meta": TinyTag.get(path, image=True) }
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
	rep = Replacement.query.filter(or_(Replacement.artist_name==artist, Replacement.artist_name==None)) \
		.filter(or_(Replacement.album_title==title, Replacement.album_title==None)).first()

	if rep:
		artist = rep.set_artist or artist
		title = rep.set_album or title
		print("Replacement! " + str(rep))

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
				artist.is_known = True
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

	for album in Album.query.all():
		try:
			# TODO: this doesn't make sense if albums are checked
			if album.picture:
				continue

			key = (album.artist.name + "/" + album.title).lower()
			if data.get(key):
				print("Using cached " + album.title + " by " + album.artist.name)
				album.picture = album.picture or data.get(key)["picture"]
				album.is_known = album.picture is not None
			else:
				print("Fetching " + album.title + " by " + album.artist.name)
				lfm_album = lastfm.get_album(album.artist.name, album.title)
				album.title = lfm_album.get_title()
				album.picture = album.picture or lfm_album.get_cover_image()
				album.is_known = True
		except pylast.WSError:
			print("Error")

	db.session.commit()


def importAllMusic():
	track_by_path = {}
	for track in Track.query.all():
		track_by_path[track.path] = track

	dir_path = os.path.dirname(os.path.realpath(__file__))

	ret = scanForMusic(app.config["MUSIC_DIR"])
	for info in ret:
		meta = info["meta"]

		if meta.title is None:
			print("Track doesn't have meta data! " + info["path"])
			continue

		album  = getOrCreateAlbum(artist=meta.albumartist or meta.artist, title=meta.album)
		artist = getOrCreateArtist(meta.artist)
		path   = info["path"]

		track = track_by_path.get(path)
		if track is None:
			print("Adding track at " + path)
			track = Track()
			db.session.add(track)

		track.album  = album
		track.artist = artist
		track.title  = meta.title
		track.path   = path

		if path in track_by_path:
			del track_by_path[track.path]

		image = meta.get_image()
		if image is not None:
			ext = getImageType(image)
			# print("Image is", ext, image[0:20])
			if ext is not None:
				filename = randomString(10) + "." + ext
				path = os.path.join(dir_path, "static/uploads/" + filename)
				with open(path, "wb") as f:
					f.write(image)

				track.picture = "/static/uploads/" + filename
				if album.picture is None:
					album.picture = track.picture

	for track in track_by_path.values():
		print("Removing missing track: " + track.path)
		db.session.delete(track)

	alb_q = Album.query.filter(~ db.exists().where(Track.album_id==Album.id))
	alb_c = alb_q.count()
	alb_q.delete(synchronize_session='fetch')

	art_q = Artist.query.filter(~ db.exists().where(or_(Track.artist_id==Artist.id, Album.artist_id==Artist.id)))
	art_c = art_q.count()
	art_q.delete(synchronize_session='fetch')

	print("Deleted {} obsolete artists and {} obsolete albums".format(art_c, alb_c))

	db.session.commit()
