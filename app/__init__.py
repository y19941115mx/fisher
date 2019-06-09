from flask import Flask
from werkzeug.utils import import_string

from app.models import db

extensions = [
    'app.ext:db',
]

blueprints = [
    'app.web:bp',
]


def register_blue_print(app):
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)


def register_plugin(app):
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

    register_blue_print(app)

    register_plugin(app)

    return app