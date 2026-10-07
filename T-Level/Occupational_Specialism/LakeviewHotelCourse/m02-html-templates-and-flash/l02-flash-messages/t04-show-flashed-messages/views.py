from flask import Blueprint, flash, redirect, render_template, url_for

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/flash-test")
def flash_test():
    flash("Flash works!", "success")
    return redirect(url_for("views.home"))


@views.route("/flash-error")
def flash_error():
    flash("Something went wrong", "error")
    return redirect(url_for("views.home"))
