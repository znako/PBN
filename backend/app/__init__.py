from config import Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)

csrf = CSRFProtect(app)

from app import routes, models
