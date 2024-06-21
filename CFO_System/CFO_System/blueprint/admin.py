from flask import flash, redirect, url_for, render_template, abort, Blueprint
from flask_login import  login_required, current_user
from CFO_System.models import *
from CFO_System.forms import *

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
@login_required
def login_protect():
    pass

# TODO: add all administrator functions
