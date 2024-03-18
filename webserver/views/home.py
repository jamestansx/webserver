from flask import Blueprint, request, render_template

home = Blueprint("home", __name__, template_folder="../templates/home")


@home.route("/", endpoint="home")
def index():
    return render_template("home/home.html")
