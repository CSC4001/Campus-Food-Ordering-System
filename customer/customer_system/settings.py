# -*- coding: utf-8 -*-

import os
import sys

from customer_system import app


# SQLite URI compatible
if sys.platform.startswith('win'):
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

SECRET_KEY = os.urandom(24)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
