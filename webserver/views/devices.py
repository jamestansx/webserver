import datetime

from flask import Blueprint, request, render_template, g, url_for
from flask_jwt_extended import create_access_token
from flask_login import login_required

from webserver.models import Data, User

def get_deviceinfo(username, device_name):
    devicelist = User.query.filter_by(username=username).first().devicelist
    for deviceinfo in devicelist:
        if deviceinfo.name == device_name:
            return deviceinfo
    else:
        return None

devices = Blueprint("devices", __name__, template_folder="../templates/devices")


@devices.route("/")
@login_required
def index():
    devicelist = User.query.filter_by(username=g.user.username).first().devicelist
    return render_template("devices/index.html", devicelist=devicelist)


@devices.route("/<string:device_name>")
@login_required
def monitor(device_name):
    deviceinfo = get_deviceinfo(g.user.username, device_name)

    if deviceinfo is None:
        abort(404, description="Device is not found")

    data = Data.query.filter_by(device_id=deviceinfo.id).order_by(Data.id.desc()).all()
    apipath = (
        url_for("api.datauser", device_name=deviceinfo.name, _external=True)
        + "?latest=true"
    )
    return render_template("devices/monitor.html", apipath=apipath)
