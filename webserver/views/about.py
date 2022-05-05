from flask import Blueprint, request, render_template

about = Blueprint("about", __name__, template_folder="../templates/about")


@about.route("/")
def index():
    return render_template("index.html")


@about.route("/projectinfo")
def projectinfo():
    return render_template("projectinfo.html")


@about.route("/members")
def members():
    return render_template("members.html")
