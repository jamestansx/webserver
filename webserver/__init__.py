import os

from flask import Flask, render_template, make_response, g
from flask_bootstrap import Bootstrap
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None, **kwargs):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "webserver.db")
    )

    app.config.from_object("webserver.config.DevelopmentConfig")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    from webserver.resources import api

    api.init_app(app)
    db.init_app(app)
    Bootstrap(app)

    login_manager = LoginManager(app)
    jwt = JWTManager(app)

    with app.app_context():
        import webserver.models

        db.create_all()

    login_manager.session_protection = "strong"
    login_manager.login_view = "users.login"

    @login_manager.user_loader
    def load_user(user_id):
        from webserver.models import User

        return User.query.filter_by(id=user_id).first()

    @app.before_request
    def before_request():
        g.user = current_user

    from webserver.views import about, error_handler, devices, home, users

    app.register_blueprint(about.about, url_prefix="/about/")
    app.register_blueprint(error_handler.error)
    app.register_blueprint(home.home, url_prefix="/")
    app.register_blueprint(devices.devices, url_prefix="/devices/")
    app.register_blueprint(users.users, url_prefix="/users/")

    return app


app = create_app()
