import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

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
