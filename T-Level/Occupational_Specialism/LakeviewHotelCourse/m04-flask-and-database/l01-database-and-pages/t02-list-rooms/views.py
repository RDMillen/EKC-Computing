from flask import Blueprint, render_template

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
