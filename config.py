import os
import password
basedir = os.path.abspath(os.path.dirname(__file__))

env_state = "prod"


class Config(object):
    if env_state == "prod":
        SQLALCHEMY_DATABASE_URI = password.SQLALCHEMY_DATABASE_URI_pord
    else:
        SQLALCHEMY_DATABASE_URI = password.SQLALCHEMY_DATABASE_URI_dev

    SECRET_KEY = password.SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
