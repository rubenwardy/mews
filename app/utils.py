import os, random, string, imghdr
from tinytag import TinyTag
import json
from . import lastfm
from .models import *
from sqlalchemy import or_
import pylast, json
from flask import redirect, url_for, abort, flash, request
from flask_login import current_user, login_user, logout_user
from flask_user import *
from functools import wraps


def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not current_user.is_authenticated:
			return redirect(url_for("user.login"))

		if not current_user.is_admin:
			abort(403)

		return f(*args, **kwargs)

	return decorated_function


def shouldReturnJSON():
	return "application/json" in request.accept_mimetypes and \
		not "text/html" in request.accept_mimetypes


def randomString(n):
	return ''.join(random.choice(string.ascii_lowercase + \
		string.ascii_uppercase + string.digits) for _ in range(n))


def _do_login_user(user, remember_me=False):
	def _call_or_get(v):
		if callable(v):
			return v()
		else:
			return v

	# User must have been authenticated
	if not user:
		return False

	db.session.commit()

	# Check if user account has been disabled
	if not _call_or_get(user.is_active):
		flash("Your account has not been enabled.", "error")
		return False

	# Use Flask-Login to sign in user
	login_user(user, remember=remember_me)
	signals.user_logged_in.send(current_app._get_current_object(), user=user)

	flash("You have signed in successfully.", "success")

	return True


def loginUser(user):
	# user_manager = current_app.user_manager
	# user_mixin = user_manager.find_user_by_username(user.username)
	return _do_login_user(user, True)
