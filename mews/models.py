from flask_sqlalchemy import SQLAlchemy
from . import app

db = SQLAlchemy(app)

class Artist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	picture = db.Column(db.String(200), unique=True, nullable=True)
	def __repr__(self):
		return "<Author %r>" % self.name


class Album(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	picture = db.Column(db.String(200), unique=True, nullable=True)

	artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"),
		nullable=False)
	artist = db.relationship("Artist",
		backref=db.backref("albums", lazy=True))

	def asDict(self):
		return {
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

	album_id = db.Column(db.Integer, db.ForeignKey("album.id"),
		nullable=False)
	album = db.relationship("Album",
		backref=db.backref("tracks", lazy=True))

	def __repr__(self):
		return "<Track %r>" % self.name


def getOrCreateAlbum(artist, title):
	art = Artist.query.filter_by(name=artist).first()
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
