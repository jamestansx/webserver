import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "d0d00473332a28451c2c009cce350a4f"
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TIMEFORMAT = "%d/%m/%Y,%H:%M:%S"


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
