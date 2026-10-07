from flask import Blueprint, render_template

views = Blueprint("views", __name__)

ROOMS = [
    {"number": 101, "type": "Single"},
    {"number": 201, "type": "Family"},
]


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/rooms")
def rooms():
    return render_template("rooms.html", rooms=ROOMS)
