from flask import make_response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from webserver.models import User


class UserLogin(Resource):
    def get(self):
        auth = request.authorization

        if auth is None:
            return make_response(
                "could not verify",
                401,
                {"WWW.Authentication": 'Basic realm: "login required"'},
            )

        user = User.query.filter_by(username=auth.username).first()

        if user is None:
            return make_response(
                "could not verify",
                401,
                {"WWW.Authentication": 'Basic realm: "login required"'},
            )

        if user.verify_password(auth.password):
            return dict(
                token=create_access_token(identity=auth.username, expires_delta=False)
            )

        return make_response(
            "could not verify",
            401,
            {"WWW.Authentication": 'Basic realm: "login required"'},
        )
