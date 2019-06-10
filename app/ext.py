from app.models import db
from flask_login import LoginManager

login_manager = LoginManager()

def setup_plugins(app):
    db.create_all(app=app)
    login_manager.login_message = '请重新登陆'
    # login_manager.login_view = 'web.auth:login'