from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods = ['GET',"POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Successfully logged in!", category="success")
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password...try again?", category="error")

    return render_template("login.html", user=current_user)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.how_to_use"))



@auth.route("/sign-up", methods = ["GET","POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        Name = request.form.get('Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already signed up!", category="error")
        elif len(email) < 4:
            flash("Email's too short!", category='error')
        elif len(Name) < 2:
            flash("Username must be longer than 1 character QQ", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 3:
            flash("At least have 3 characters for your password, c'mon!", category="error")
        else:
            new_User = User(email=email, Name=Name, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_User)
            db.session.commit()
            login_user(new_User, remember = True)
            flash("User created!", category="success")
            return redirect(url_for("views.home"))


    return render_template("sign_up.html", user=current_user)


