from datetime import date

from flask import Flask as _Flask
from werkzeug.utils import import_string
from flask.json import JSONEncoder as _JSONEncoder


from app.ext import setup_plugins
from app.libs.exception import ApiException


extensions = [
    'app.ext:db',
    'app.ext:login_manager',
    'app.ext:cache',
    'app.ext:mail',
]

blueprints = [
    'app.web:bp',
    'app.api.v1:bp'
]


def register_blue_prints(app):
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)


def register_plugins(app):
    for ext_name in extensions:
        ext = import_string(ext_name)
        ext.init_app(app)


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


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ApiException()


class Flask(_Flask):
    json_encoder = JSONEncoder