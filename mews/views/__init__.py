from flask import render_template, redirect, url_for, send_file, abort, request, jsonify, flash
from flask_user import login_required, current_user
from mews import app
from mews.models import *
from mews.utils import loginUser

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


@app.route("/invites/<invite>/")
def login_invite(invite):
	user = User.query.filter_by(invite=invite).first()
	if user is None:
		abort(404)

	if current_user.is_authenticated:
		flash("You are already logged in!", "warning")
		return redirect(url_for("hello"))


	if user.is_admin:
		abort(403)

	loginUser(user)

	user.invite = None
	db.session.commit()

	return redirect(url_for("hello"))


from . import sass, api, admin, dummyart
