from flask import current_app, flash, url_for, redirect
from flask_login import login_required, current_user

from app.libs.redprint import Redprint
from app.models import db
from app.models.gift import Gift

redprint = Redprint('gifts')


@redprint.route('/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            gift.add()
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
        flash('添加成功！')
    else:
        flash('添加失败！')

    return redirect(url_for('web.book:detail', isbn=isbn))
