from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FieldList
from wtforms.validators import DataRequired, EqualTo, Length

from webserver.models import User


class UserRegisterForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(max=150)]
    )
    password = PasswordField(
        label="New Password",
        validators=[DataRequired(), EqualTo("confirm", message="Passwords must match")],
    )
    confirm = PasswordField(label="Repeat Password")

    def validate(self):
        initial_validation = super(UserRegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        return True


class UserLoginForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(max=150)]
    )
    password = PasswordField(label="Password", validators=[DataRequired()])

    def validate(self):
        initial_validation = super(UserLoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append("Unknown username")
            return False
        if not user.verify_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False
        return True


class DeviceRegisterForm(FlaskForm):
    devicename = StringField(
        label="Device Name", validators=[DataRequired(), Length(max=150)]
    )
    datatypes = FieldList(StringField("Name"), min_entries=1)

    def validate(self):
        initial_validation = super(DeviceRegisterForm, self).validate()
        if not initial_validation:
            return False

        if not isinstance(self.datatypes.data, list):
            return False

        user = User.query.filter_by(username=g.user.username).first()
        for i in user.devicelist:
            print(self.devicename.data)
            print(i.name)
            if self.devicename.data == i.name:
                self.devicename.errors.append(f"Name '{self.devicename.data}' is used")
                return False
        return True
