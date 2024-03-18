from flask_restful import Api

api = Api(prefix="/api")

from webserver.resources.user_login import UserLogin
from webserver.resources.device_data import DeviceData, DataWLogin

api.add_resource(UserLogin, "/user/login", endpoint="api.userlogin")
api.add_resource(
    DeviceData, "/device/<string:device_name>/data", endpoint="api.devicedata"
)
api.add_resource(
    DataWLogin, "/user/device/<string:device_name>/data", endpoint="api.datauser"
)
