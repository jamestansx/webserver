from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from webserver import db


class TimestampMixin(object):
    time_collected = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    devicelist = db.relationship("DeviceInfo", backref="user")

    def __repr__(self):
        return f"<User {repr(self.username)}>"

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class DeviceInfo(TimestampMixin, db.Model):
    __tablename__ = "deviceinfo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(150), unique=True)
    datatype = db.relationship("DataType", backref="deviceinfo")

    def __repr__(self):
        return f"<Device {repr(self.name)}>"


class DataType(db.Model):
    __tablename__ = "datatype"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("deviceinfo.id"))
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<DataType {repr(self.name)}>"


class Data(TimestampMixin, db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("deviceinfo.id"))
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Data {repr(self.device_id)}>"
