from flask import Blueprint, flash, redirect, url_for

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return "Welcome to Lakeview Hotel"


@views.route("/flash-test")
def flash_test():
    flash("Flash works!", "success")
    return redirect(url_for("views.home"))
