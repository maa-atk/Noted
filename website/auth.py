
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
# using mixiin function for
from flask_login import login_required, login_user, logout_user, current_user
# for password safe store (one way hash)
auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")  # for only forms nothing else
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f"Welcome {user.first_name}", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home', user=current_user))
            else:
                flash('Incorrect Password , try again',
                      category="error")
        else:
            flash('Not Registered ',
                  category="error")

    return render_template("login.html", user=current_user)
# add variables to send here "testing"


@auth.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 10:
            flash('Email must be greater than 10 char',
                  category="error")  # for flashing cards
            pass
        if password1 != password2:
            flash('Passwords Do not match',
                  category="error")  # for flashing cards
            pass
        else:
            # add user function for adding user
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists", category="success")

            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember=True)
                flash("Account created", category="success")
            # safer route
                return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)
