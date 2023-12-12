#for login, signin, signup, etc

from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/log-in", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        usr = User.query.filter_by(email=email).first()
        if usr:
            if check_password_hash(usr.password, password):
                flash('Logged In!', category='success')
                login_user(usr, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        emailExists = User.query.filter_by(email=email).first()
        usernameExists = User.query.filter_by(username=username).first()

        if emailExists:
            flash('Email is already used by another user!', category='error')
        elif usernameExists:
            flash('Username is already used by another user!', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password1) < 6:
            flash('Password is too short', category='error')
        elif len(email) < 4:
            flash('Email is invalid', category='error')
        else:
            newUser = User(email=email,username=username,password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('User has been created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/log-out")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("views.home"))

