from flask import render_template, redirect, url_for, send_file, abort, request, jsonify, flash
from flask_user import login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from mews import app, lastfm
from mews.utils import scanForMusic, getArtistsInfo, getAlbumsInfo, importAllMusic
from mews.models import *


@app.route("/admin/")
@login_required
def admin():
	unknown_albums = Album.query.filter_by(is_known=False).order_by(Album.title).all()
	unknown_artists = Artist.query.filter_by(is_known=False).order_by(Artist.name).all()
	unknown_tracks = Track.query.filter_by(is_known=False).order_by(Track.title).all()
	return render_template("admin/index.html",
			unknown_albums=unknown_albums, unknown_artists=unknown_artists, unknown_tracks=unknown_tracks,
			num_artists=Artist.query.count(), num_albums=Album.query.count(), num_tracks=Track.query.count(),
			replacements=Replacement.query.all())


class ReplacementForm(FlaskForm):
	album_title = StringField("Album")
	artist_name = StringField("Album Artist")
	set_album   = StringField("Set Album")
	set_artist  = StringField("Set Album Artist")


@app.route("/admin/replacements/new/", methods=["GET", "POST"])
@login_required
def replacement_new():
	form = ReplacementForm(request.form)
	if form.validate_on_submit():
		rep = Replacement()
		form.populate_obj(rep)
		rep.fixEmptyFields()
		if rep.isValid():
			db.session.add(rep)
			db.session.commit()

			flash("Added placement: " + str(rep))

			return redirect(url_for('admin'))

	return render_template("admin/replacement_new.html", form=form)


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
