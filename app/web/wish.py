from app.libs.redprint import Redprint
from flask_login import login_required, current_user
from flask import redirect, url_for, flash

from app.models import db
from app.models.wish import Wish 

redprint = Redprint('wish')


@redprint.route('/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            wish.add()
        flash('添加成功！')
    else:
        flash('添加失败')
    return redirect(url_for('web.book:detail', isbn=isbn))


@redprint.route('/satisfy/<int:wid>')
def satisfy_wish(wid):
    return 'hello'
