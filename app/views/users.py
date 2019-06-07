from flask import render_template, redirect, url_for, abort, request, flash
from flask_user import login_required, current_user, user_manager, signals, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Length, Optional, Email
from app import app, lastfm
from app.utils import admin_required, randomString
from app.models import *
from app.utils import loginUser


class UserProfileForm(FlaskForm):
	display_name = StringField("Display name", [Optional(), Length(2, 20)])
	submit = SubmitField("Save")


@app.route("/users/<username>/", methods=["GET", "POST"])
def user_profile_page(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		abort(404)

	form = None
	if current_user.is_authenticated and (current_user == user or current_user.is_admin):
		form = UserProfileForm(formdata=request.form, obj=user)
		if form.validate_on_submit():
			db.session.commit()
			return redirect(url_for("user_profile_page", username=username))

	return render_template("users/user_profile_page.html",
			user=user, form=form)


class SetPasswordForm(FlaskForm):
	password = PasswordField("New password", [InputRequired(), Length(2, 20)])
	password2 = PasswordField("Verify password", [InputRequired(), Length(2, 20)])
	submit = SubmitField("Save")


@app.route("/user/set-password/", methods=["GET", "POST"])
@login_required
def set_password_page():
	if current_user.password != "":
		return redirect(url_for("user.change_password"))

	form = SetPasswordForm(request.form)

	if request.method == "POST" and form.validate():
		one = form.password.data
		two = form.password2.data
		if one == two:
			current_user.password = user_manager.hash_password(form.password.data)
			current_user.invite = None
			db.session.commit()

			signals.user_changed_password.send(current_app._get_current_object(), user=current_user)

			flash('Your password has been changed successfully.', 'success')
			return redirect(url_for("user.login"))
		else:
			flash("Passwords do not match", "error")

	return render_template("users/set_password.html", form=form, optional=request.args.get("optional"))


@app.route("/invites/<invite>/")
def login_invite(invite):
	user = User.query.filter_by(invite=invite).first()
	if user is None:
		abort(404)

	if current_user.is_authenticated:
		flash("You are already logged in!", "warning")
		return redirect(url_for("hello"))

	if user.is_admin or user.password != "":
		abort(403)

	loginUser(user)
	db.session.commit()

	return redirect(url_for("set_password_page"))
