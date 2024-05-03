from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64, os
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User
import io, base64

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.save()
        flash('Your account has been created. You may now login')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("snippets.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("users.account"))
        flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('snippets.index'))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            update_username_form.validate_username(update_username_form.username)
            current_user.modify(username=update_username_form.username.data)
            current_user.save()
            flash('Your username has been updated.')
            return redirect(url_for('users.account'))

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            image = update_profile_pic_form.picture.data
            secure_filename(image.filename)
            current_user.profile_pic.replace(image.stream, content_type='images/png')
            current_user.save()
            return redirect(url_for('users.account'))

    def get_b64_img(username):
        user = User.objects(username=username).first()
        bytes_im = io.BytesIO(user.profile_pic.read())
        image = base64.b64encode(bytes_im.getvalue()).decode()
        return image
    img = get_b64_img(current_user.username)
    return render_template("account.html", title="Account", update_username_form=update_username_form, update_profile_pic_form=update_profile_pic_form, image=img)