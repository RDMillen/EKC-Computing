from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connection

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")
@views.route("/profile")
def profile():
    if "username" in session:
        args = request.args
        name = args.get('nm')
        return render_template("profile.html", name=session["username"])
    else:
        return redirect(url_for("views.login"))

@views.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        return redirect(url_for("views.profile"))
    elif request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        # Parse user data to main database.
        connection = db_connection()
        connection.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash)
        )
        connection.commit()
        connection.close()

        session.permanent = True
        session["username"] = username

        return redirect(url_for("views.login"))

    else:
        return render_template("register.html")

@views.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = db_connection()
        username = connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.close()

        if username and check_password_hash(username["password_hash"], password):
            session["username"] = username["username"]
            return redirect(url_for("views.profile"))

        return redirect(url_for("views.profile"))
    else:
        if "username" in session:
            return redirect(url_for("views.profile"))
        return render_template("login.html")

@views.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("views.login"))


@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))
