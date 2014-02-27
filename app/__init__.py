
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_path="/app/static")
app.config.from_object("config")
app.debug = True
db = SQLAlchemy(app)

from . import views

