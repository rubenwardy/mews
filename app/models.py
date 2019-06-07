from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin, current_app
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy
from . import app, lastfm
import json

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
	username = db.Column(db.String(20, collation='NOCASE'), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, default="")
	is_admin = db.Column(db.Boolean, nullable=False, default=False)
	invite = db.Column(db.String(32), nullable=True, default=None)

	def __eq__(self, other):
		return self.id == other.id


user_manager = UserManager(app, db, User)


class Artist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	picture = db.Column(db.String(200), unique=True, nullable=True)
	is_known = db.Column(db.Boolean, nullable=False, default=False)

	def asDict(self, add_id=True):
		dict = {
			"name": self.name,
			"picture": self.picture
		}

		if add_id:
			dict["id"] = self.id

		return dict

	def __repr__(self):
		return "<Author %r>" % self.name


class Album(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	picture = db.Column(db.String(200), unique=False, nullable=True)
	is_known = db.Column(db.Boolean, nullable=False, default=False)
	num_tracks = db.Column(db.Integer, nullable=True, default=None)

	artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"),
		nullable=False)
	artist = db.relationship("Artist",
		backref=db.backref("albums", lazy=True))

	def getPictureURL(self):
		if self.picture and self.picture[0:46] == "https://lastfm-img2.akamaized.net/i/u/300x300/":
			return url_for("thing_art", file=self.picture[46:])
		else:
			return self.picture

	def asDict(self, add_id=True):
		dict = {
			"title": self.title,
			"artist": self.artist.name,
			"picture": self.getPictureURL()
		}

		if add_id:
			dict["id"] = self.id

		return dict

	def __repr__(self):
		return "<Album %r>" % self.name


class PlaylistTrack(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
	track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
	position = db.Column(db.Integer)
	track = db.relationship("Track")

	def __init__(self, track=None):
		self.track = track


class Track(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	number = db.Column(db.Integer, nullable=True)
	picture = db.Column(db.String(200), unique=False, nullable=True)
	path = db.Column(db.String(80), unique=True, nullable=False)
	is_known = db.Column(db.Boolean, nullable=False, default=False)
	position = db.Column(db.Integer, nullable=True, default=None)

	artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"),
		nullable=False)
	artist = db.relationship("Artist",
		backref=db.backref("tracks", lazy=True))

	album_id = db.Column(db.Integer, db.ForeignKey("album.id"),
		nullable=False)
	album = db.relationship("Album",
		backref=db.backref("tracks", lazy=True, order_by=lambda: Track.position))

	def asDict(self, pt_id=None, add_id=True):
		dict = {
			"title": self.title,
			"artist": self.artist.name,
			"picture": self.picture or self.album.picture,
			"pt_id": pt_id
		}

		if add_id:
			dict["id"] = self.id

		return dict

	def __repr__(self):
		return "<Track {} {} {}>".format(self.title, self.artist.name, self.position)



class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)

	_tracks = db.relationship(PlaylistTrack,
		order_by=[PlaylistTrack.position],
		collection_class=ordering_list('position'))

	tracks = association_proxy('_tracks', 'track')

	def asDict(self):
		return {
			"id": self.id,
			"title": self.title,
			"count": len(self.tracks)
		}

	def __repr__(self):
		return "<Playlist %r>" % self.title


class Replacement(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	album_title = db.Column(db.String(80), nullable=True)
	artist_name = db.Column(db.String(80), nullable=True)
	set_album   = db.Column(db.String(80), nullable=True)
	set_artist  = db.Column(db.String(80), nullable=True)

	def __str__(self):
		ret = ""

		if self.album_title:
			ret += "Album " + self.album_title
			if self.artist_name:
				ret += " by " + self.artist_name

		elif self.artist_name:
			ret += "Artist " + self.artist_name

		if self.set_album:
			ret += " is actually album " + self.set_album
			if self.set_artist:
				ret += " by " + self.set_artist
		elif self.album_title and self.set_artist == "Various Artists":
			ret += " is actually a compilation by Various Artists"
		elif self.set_artist:
			if self.album_title:
				ret += " is actually by " + self.set_artist
			elif self.artist_name:
				ret += " is actually called " + self.set_artist
			else:
				assert(False)


		return ret

	def fixEmptyFields(self):
		if self.album_title.strip() == "":
			self.album_title = None

		if self.artist_name.strip() == "":
			self.artist_name = None

		if self.set_album.strip() == "":
			self.set_album = None

		if self.set_artist.strip() == "":
			self.set_artist = None

	def isValid(self):
		return (self.album_title or self.artist_name) and (self.set_album or self.set_artist)
