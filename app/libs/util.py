import random
import string
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from werkzeug.exceptions import InternalServerError

from app.ext import mail


def is_isbn_or_key(word):
    word = word.strip()
    isbn_or_key = 'key'
    if check_isbn(isbn_or_key):
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
            raise InternalServerError()


def send_email(to: str, subject: str, template: str, **kwargs):
    app = current_app._get_current_object()
    msg = Message('[鱼书]' + ' ' + subject, recipients=[to])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr
