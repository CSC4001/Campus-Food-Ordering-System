from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()

@login_manager.user_loader
def load_admin(user_id):
    from CFO_System.models import Administrator
    admin = Administrator.query.get(int(user_id))
    return admin

@login_manager.user_loader
def load_user(user_id):
    from CFO_System.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'
