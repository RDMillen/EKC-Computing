from flask import Blueprint, render_template

views = Blueprint("views", __name__)

ROOMS = [
    {"number": 101, "type": "Single", "price": 80.0, "available": True},
    {"number": 102, "type": "Double", "price": 120.0, "available": False},
    {"number": 201, "type": "Family", "price": 180.0, "available": True},
]


@views.route("/rooms")
def rooms():
    return render_template("rooms.html", rooms=ROOMS)
