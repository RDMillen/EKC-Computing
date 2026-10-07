import functools
import sqlite3

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/rooms")
def rooms():
    db = get_db()
    all_rooms = db.execute(
        "SELECT id, number, room_type, capacity, price_per_night, available "
        "FROM rooms ORDER BY number"
    ).fetchall()
    return render_template("rooms.html", rooms=all_rooms)


def parse_room_form(form):
    """Validate the add-room form. Returns (room_dict, None) or (None, error_message)."""
    values = {key: form.get(key, "").strip() for key in ("number", "room_type", "capacity", "price_per_night")}
    if not all(values.values()):
        return None, "Please fill in all fields"
    try:
        room = {
            "number": int(values["number"]),
            "room_type": values["room_type"],
            "capacity": int(values["capacity"]),
            "price_per_night": float(values["price_per_night"]),
        }
    except ValueError:
        return None, "Number, capacity and price must be numbers"
    if room["capacity"] < 1 or room["price_per_night"] <= 0:
        return None, "Capacity and price must be greater than zero"
    return room, None


@views.route("/rooms/new", methods=["GET", "POST"])
def new_room():
    if request.method == "POST":
        room, error = parse_room_form(request.form)
        if error:
            flash(error, "error")
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO rooms (number, room_type, capacity, price_per_night) "
                    "VALUES (?, ?, ?, ?)",
                    (room["number"], room["room_type"], room["capacity"], room["price_per_night"]),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("That room number already exists", "error")
            else:
                flash("Room added", "success")
                return redirect(url_for("views.rooms"))
    return render_template("room_form.html", form=request.form)


@views.route("/rooms/<int:room_id>")
def room_detail(room_id):
    db = get_db()
    room = db.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
    if room is None:
        abort(404)
    return render_template("room_detail.html", room=room)


@views.before_app_request
def load_logged_in_user():
    """Make the logged-in user (or None) available as g.user on every request."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not (name and email and password):
            flash("Please fill in all fields", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters", "error")
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("That email is already registered", "error")
            else:
                flash("Registered successfully. Please log in.", "success")
                return redirect(url_for("views.login"))
    return render_template("register.html", form=request.form)


@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash("Welcome back, " + user["name"], "success")
            return redirect(url_for("views.rooms"))
    return render_template("login.html", form=request.form)


@views.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("views.login"))


def login_required(view):
    """Decorator: send anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("Please log in first", "error")
            return redirect(url_for("views.login"))
        return view(*args, **kwargs)

    return wrapped_view


@views.route("/account")
@login_required
def account():
    return render_template("account.html")
