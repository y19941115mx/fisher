from flask import Flask
from werkzeug.utils import import_string

from app.ext import setup_plugins

extensions = [
    'app.ext:db',
    'app.ext:login_manager',
]

blueprints = [
    'app.web:bp',
]


def register_blue_prints(app):
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)


def register_plugins(app):
    for ext_name in extensions:
        ext = import_string(ext_name)
        ext.init_app(app)
        if ext_name == 'app.ext:db':
            ext.create_all(app=app)


def create_app(debug=True):
    app = Flask(__name__)

    if debug:
        app.config.from_object('config.dev')
    else:
        app.config.from_object('config.proc')

    register_blue_prints(app)

    register_plugins(app)

    setup_plugins(app)

    return app