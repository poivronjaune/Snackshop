from flask import Blueprint, flash, render_template, redirect, request, url_for
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get("email")
        password = request.form.get("password")
        print(f"email   : {email}")
        print(f"pw1     : {password}")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
        
        flash('Bad credentials, please try again!', category='error')
   
    return render_template("login.html")


@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        email    = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        print(f"username: {username}")
        print(f"email   : {email}")
        print(f"pw1     : {password1}")
        print(f"pw2     : {password2}")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email already in use.', category='error')
        elif username_exists:
            flash('Username already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 8:
            flash('Password length is too short. (Min length is 8)', category='error')
        elif len(email) < 5:
            flash('Email is too short. (Min length is 5)', category='error')
            # TODO: Add regex check to validate email format
        else:
            pw_hash = generate_password_hash(password=password1, method='sha256')
            new_user = User(email=email, username=username, password=pw_hash)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
