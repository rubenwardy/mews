from flask import render_template, redirect, url_for, send_file, abort, request, jsonify, flash, send_from_directory
from flask_user import login_required, current_user
from app import app
from app.models import *
import os, urllib.request


@user_manager.login_manager.unauthorized_handler
def unauthorized():
	#   if request.path.startswith('/api/'):
	return jsonify(success=False,
			data={'login_required': True},
			message='Authorize please to access this page.'), 401
	#   else:
	#   abort(500)
	#   return redirect(url_for('auth.signin'))

assert(user_manager.login_manager.unauthorized_callback == unauthorized)


@app.route("/")
def hello():
	return render_template("home.html")


@app.route("/tracks/<int:id>/")
@login_required
def track_file(id):
	track = Track.query.get(id)
	if track is None:
		print("No track!")
		abort(404)

	print(track.path)
	return send_file(track.path)


@app.route("/art/<file>")
def thing_art(file):
	dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../static/uploads/")
	filepath = os.path.join(dir_path, file)
	print(filepath)
	if not os.path.isfile(filepath):
		urllib.request.urlretrieve("https://lastfm-img2.akamaized.net/i/u/300x300/" + file, filepath)


	return send_from_directory(dir_path, file)


from . import sass, api, admin, dummyart, users
