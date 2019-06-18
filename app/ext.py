from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail

from app.models import db


login_manager = LoginManager()

cache = Cache(config={'CACHE_TYPE': 'simple'})

mail = Mail()


def setup_plugins(app):
    # 配置插件
    login_manager.login_message = '请重新登陆'
    login_manager.login_view = 'web.auth:login'