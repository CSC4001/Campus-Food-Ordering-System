# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('customer_system')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
CORS(app)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from customer_system import views, errors, commands
