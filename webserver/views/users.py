import secrets
from flask import Blueprint, request, render_template, url_for, redirect, g
from flask_login import login_user, logout_user, login_required
from webserver.forms import UserRegisterForm, UserLoginForm, DeviceRegisterForm
from webserver import db
from webserver.models import User, DeviceInfo, DataType

users = Blueprint("users", __name__, template_folder="../templates/users")


@users.route("/register/", methods=["GET", "POST"])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home.home"))
    return render_template("register.html", form=form)


@users.route("/login/", methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            redirect_url = url_for("home.home")
            return redirect(redirect_url)
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))


@users.route("/device/register", methods=["GET", "POST"])
def device_register():
    form = DeviceRegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=g.user.username).first()
        user.devicelist.append(
            DeviceInfo(
                name=form.devicename.data,
                datatype=[DataType(name=datatype) for datatype in form.datatypes.data],
            )
        )
        db.session.commit()
        return redirect(url_for("home.home"))
    return render_template("device_register.html", form=form)
