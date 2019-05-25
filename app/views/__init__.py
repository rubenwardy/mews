from flask import render_template, redirect, url_for, send_file, abort, request, jsonify, flash
from flask_user import login_required, current_user
from app import app
from app.models import *


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


from . import sass, api, admin, dummyart, users
