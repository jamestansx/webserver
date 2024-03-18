from datetime import datetime

from flask import abort, current_app, g, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_required
from flask_restful import Resource, reqparse

from webserver import db
from webserver.common.utils import *
from webserver.models import Data, DeviceInfo, User

parser = reqparse.RequestParser()
parser.add_argument("data", type=dict, location="json", required=True)
parser.add_argument("time_collected", type=str, location="json")


class DeviceData(Resource):
    @jwt_required()
    def get(self, device_name):
        username = get_jwt_identity()
        deviceinfo = get_deviceinfo(username, device_name)
        is_latest = request.args.get(
            "latest", default=False, type=lambda x: x.lower() == "true"
        )

        if deviceinfo is None:
            abort(404, description="API Key is invalid")

        data_query = Data.query.filter_by(device_id=deviceinfo.id).all()

        payload = dict()

        payload["device_name"] = deviceinfo.name
        payload["device_id"] = deviceinfo.id
        payload["datatype"] = [datatype.name for datatype in deviceinfo.datatype]
        payload["data"] = list()
        for index, data in enumerate(data_query):
            data.data["time_collected"] = data.time_collected.strftime(
                current_app.config["TIMEFORMAT"]
            )
            payload["data"].append(data.data)
            if is_latest and index == 0:
                print("tste")
                break

        return payload

    @jwt_required()
    def post(self, device_name):
        args = parser.parse_args()
        username = get_jwt_identity()
        deviceinfo = get_deviceinfo(username, device_name)

        if deviceinfo is None:
            abort(404, description="Device is not found")

        if not self.validate_data(args["data"], deviceinfo):
            abort(406, description="Data types aren't matched with database")

        new_data = Data(device_id=deviceinfo.id, data=args["data"])

        if args["time_collected"] is not None:
            try:
                time_collected = datetime.strptime(
                    args["time_collected"], current_app.config["TIMEFORMAT"]
                )
            except ValueError:
                abort(
                    406,
                    description=f"date format should be {current_app.config['TIMEFORMAT']}",
                )

            new_data.time_collected = time_collected
        db.session.add(new_data)
        db.session.commit()
        return 200

    def validate_data(self, data, deviceinfo):
        if len(data) != len(deviceinfo.datatype):
            return False
        for datatype in deviceinfo.datatype:
            if datatype.name not in data.keys():
                return False
        return True


class DataWLogin(Resource):
    @login_required
    def get(self, device_name):
        username = g.user.username
        deviceinfo = get_deviceinfo(username, device_name)
        is_latest = request.args.get(
            "latest", default=False, type=lambda x: x.lower() == "true"
        )

        if deviceinfo is None:
            abort(404, description="API Key is invalid")

        data_query = Data.query.filter_by(device_id=deviceinfo.id)

        payload = dict()

        payload["device_name"] = deviceinfo.name
        payload["device_id"] = deviceinfo.id
        payload["datatype"] = [datatype.name for datatype in deviceinfo.datatype]
        payload["data"] = list()
        if is_latest:
            data_query = [data_query.order_by(Data.id.desc()).first()]
        for data in data_query:
            data.data["time_collected"] = data.time_collected.strftime(
                current_app.config["TIMEFORMAT"]
            )
            payload["data"].append(data.data)

        return payload

    def validate_data(self, data, deviceinfo):
        if len(data) != len(deviceinfo.datatype):
            return False
        for datatype in deviceinfo.datatype:
            if datatype.name not in data.keys():
                return False
        return True
