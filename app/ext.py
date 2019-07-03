import logging

from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail

from app.models import db


login_manager = LoginManager()

cache = Cache(config={'CACHE_TYPE': 'simple'})

mail = Mail()


def setup_plugins(app):
    # 配置插件
    db.create_all(app=app)
    login_manager.login_message = '请重新登陆'
    login_manager.login_view = 'web.auth:login'

    # 配置日志
    if not app.config['DEBUG']:
        logging.basicConfig(filename="app.log", filemode='w',
                            format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
