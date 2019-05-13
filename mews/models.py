from flask_sqlalchemy import SQLAlchemy
from . import app, lastfm
import json

db = SQLAlchemy(app)

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


playlist_tracks = db.Table("playlist_tracks",
	db.Column("playlist_id", db.Integer, db.ForeignKey("playlist.id"), primary_key=True),
	db.Column("track_id",    db.Integer, db.ForeignKey("track.id"), primary_key=True)
)


class Playlist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)

	tracks = db.relationship("Track", secondary=playlist_tracks, lazy="dynamic",
		backref=db.backref("playlists", lazy="dynamic"))

	def asDict(self):
		return {
			"id": self.id,
			"title": self.title,
			"count": self.tracks.count()
		}

	def __repr__(self):
		return "<Playlist %r>" % self.title
