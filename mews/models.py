from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy
from . import app, lastfm
import json

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
	username = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')
	email_confirmed_at = db.Column(db.DateTime())

user_manager = UserManager(app, db, User)


class Artist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	picture = db.Column(db.String(200), unique=True, nullable=True)
	is_known = db.Column(db.Boolean, nullable=False, default=False)

	def asDict(self):
		return {
			"id": self.id,
			"name": self.name,
			"picture": self.picture
		}

	def __repr__(self):
		return "<Author %r>" % self.name


class Album(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	picture = db.Column(db.String(200), unique=True, nullable=True)
	is_known = db.Column(db.Boolean, nullable=False, default=False)

	artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"),
		nullable=False)
	artist = db.relationship("Artist",
		backref=db.backref("albums", lazy=True))

	def asDict(self):
		return {
			"id": self.id,
			"title": self.title,
			"artist": self.artist.name,
			"picture": self.picture
		}

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
	picture = db.Column(db.String(200), unique=True, nullable=True)
	path = db.Column(db.String(80), unique=True, nullable=False)
	is_known = db.Column(db.Boolean, nullable=False, default=False)

	artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"),
		nullable=False)
	artist = db.relationship("Artist",
		backref=db.backref("tracks", lazy=True))

	album_id = db.Column(db.Integer, db.ForeignKey("album.id"),
		nullable=False)
	album = db.relationship("Album",
		backref=db.backref("tracks", lazy=True))

	def asDict(self, pt_id=None):
		return {
			"id": self.id,
			"title": self.title,
			"artist": self.artist.name,
			"picture": self.picture or self.album.picture,
			"pt_id": pt_id
		}

	def __repr__(self):
		return "<Track %r>" % self.title


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
