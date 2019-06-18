from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models import db


def generate_token(data=None, expiration=None):
    if data is None:
        data = {}
    expiration = expiration or current_app.config.get('EXPIRATION_TIME', 600)
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps(data).decode('ascii')


def translate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('ascii'))
    except:
        return None
    return data