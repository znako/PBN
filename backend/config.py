import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "really-sercret-key"
    SQLALCHEMY_DATABASE_URI = "mysql://root:RootPassword@localhost:3306/meow_site"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
