from webserver.models import User


def get_deviceinfo(username, device_name):
    devicelist = User.query.filter_by(username=username).first().devicelist
    for deviceinfo in devicelist:
        if deviceinfo.name == device_name:
            return deviceinfo
    return None
