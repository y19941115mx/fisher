import json
import random
import string
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app.ext import mail
from .exception import ApiException
from app.models import Base
from flask import jsonify as _jsonify


def is_isbn_or_key(word):
    word = word.strip()
    isbn_or_key = 'key'
    if check_isbn(word):
        isbn_or_key = 'isbn'
    return isbn_or_key


def check_isbn(isbn):
    isbn = isbn.strip()
    if len(isbn) == 13 and isbn.isdigit():
        return True
    short_word = isbn.replace('-', '')
    if len(short_word) == 10 and short_word.isdigit():
        return True
    return False


def generate_secret_key(n=50):
    seed = string.ascii_letters + '1234567890'
    sa = []
    for i in range(n):
        sa.append(random.choice(seed))

    salt = ''.join(sa)
    return salt


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.exception('email send fail')


def send_email(to: str, subject: str, template: str, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[鱼书]' + ' ' + subject, recipients=[to])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr


def jsonify(data=None, code=200, **kwargs):
    if isinstance(data, Base):
        for k, v in kwargs.items():
            setattr(data, k, v)
            data.append(k)
        data = dict(data=data, msg='success', code=None)
    elif isinstance(data, list):
        data = dict(data=data, msg='success', code=None)
        for k, v in kwargs.items():
            setattr(data, k, v)

    return _jsonify(**kwargs), code
