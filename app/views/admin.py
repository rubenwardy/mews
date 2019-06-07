from flask import render_template, redirect, url_for, send_file, abort, request, jsonify, flash
from flask_user import login_required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from app import app, lastfm
from app.utils import admin_required, randomString
from app.tasks.tasks import syncAlbums, syncArtists, syncMusic
from app.models import *
from sqlalchemy import func


@app.route("/admin/")
@admin_required
def admin():
	unknown_albums = Album.query.filter_by(is_known=False).order_by(Album.title).all()
	unknown_artists = Artist.query.filter_by(is_known=False).order_by(Artist.name).all()
	unknown_tracks = Track.query.filter_by(is_known=False).order_by(Track.title).all()
	missing_album_art = Album.query.filter_by(picture=None).order_by(Album.title).all()

	# incomplete_albums = Album.query \
	# 		.filter(Album.num_tracks!=None) \
	# 		.join(Album.tracks) \
	# 		.filter(func.count(Album.num_tracks) == Album.num_tracks) \
	# 		.all()

	albums = Album.query.filter(Album.num_tracks != None).join(Artist.albums).order_by(Artist.name).all()
	incomplete_albums = [a for a in albums if a.num_tracks > len(a.tracks)]
	overflow_albums = [a for a in albums if a.num_tracks < len(a.tracks)]
	no_pos_tracks = Track.query.filter(Track.position==None).all()

	users = User.query.order_by(User.is_admin.desc(), User.username).all()
	return render_template("admin/index.html",
			unknown_albums=unknown_albums, unknown_artists=unknown_artists, unknown_tracks=unknown_tracks,
			num_artists=Artist.query.count(), num_albums=Album.query.count(), num_tracks=Track.query.count(),
			incomplete_albums=incomplete_albums, overflow_albums=overflow_albums, no_pos_tracks=no_pos_tracks,
			replacements=Replacement.query.all(), missing_album_art=missing_album_art, users=users)


class ReplacementForm(FlaskForm):
	album_title = StringField("Album")
	artist_name = StringField("Album Artist")
	set_album   = StringField("Set Album")
	set_artist  = StringField("Set Album Artist")


@app.route("/admin/replacements/new/", methods=["GET", "POST"])
@admin_required
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


@app.route("/admin/replacements/<int:id>/edit/", methods=["GET", "POST"])
@admin_required
def replacement_edit(id):
	rep = Replacement.query.get(id)
	if rep is None:
		abort(404)

	form = ReplacementForm(request.form, obj=rep)
	if form.validate_on_submit():
		form.populate_obj(rep)
		rep.fixEmptyFields()
		if rep.isValid():
			db.session.commit()

			flash("Added placement: " + str(rep))

			return redirect(url_for('admin'))

	return render_template("admin/replacement_edit.html", form=form, rep=rep)


@app.route("/admin/replacements/<int:id>/delete/", methods=["POST"])
@admin_required
def replacement_delete(id):
	Replacement.query.filter_by(id=id).delete()
	db.session.commit()

	return redirect(url_for('admin'))


class InviteForm(FlaskForm):
	username = StringField("Username", [DataRequired(), Length(min=4, max=20)])
	invite = StringField("Invite", [DataRequired(), Length(32)], render_kw={"readonly": True})


@app.route("/admin/invite/", methods=["GET", "POST"])
@admin_required
def invite():
	form = InviteForm(request.form)
	if request.method == "GET":
		form.invite.data = randomString(32)

	if form.validate_on_submit():
		username = form.username.data
		if User.query.filter_by(username=username).first() is None:
			user = User()
			user.username = username
			user.invite = form.invite.data
			print(form.invite.data)
			assert(len(form.invite.data) == 32)
			db.session.add(user)
			db.session.commit()

			flash("Created username and for " + username, "success")
			return redirect(url_for('admin'))
		else:
			flash("User " + username + " already exists", "danger")

	return render_template("admin/invite.html", form=form)


@app.route("/admin/sync/albums/", methods=["POST"])
@admin_required
def sync_album():
	ret = syncAlbums.delay()
	flash("Syncing album meta data", "success")
	return redirect(url_for("check_task", id=ret.id, r=url_for("admin")))


@app.route("/admin/sync/artists/", methods=["POST"])
@admin_required
def sync_artist():
	ret = syncArtists.delay()
	flash("Syncing artist meta data", "success")
	return redirect(url_for("check_task", id=ret.id, r=url_for("admin")))


@app.route("/admin/sync/music/", methods=["POST"])
@admin_required
def sync_music():
	ret = syncMusic.delay()
	flash("Importing music from file system", "success")
	return redirect(url_for("check_task", id=ret.id, r=url_for("admin")))
