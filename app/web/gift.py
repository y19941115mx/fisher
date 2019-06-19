from flask import current_app, flash, url_for, redirect, render_template
from flask_login import login_required, current_user

from app.libs.redprint import Redprint
from app.models import db
from app.models.gift import Gift
from app.view_models.trade import MyTrades

redprint = Redprint('gift')


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


@redprint.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    my_gifts = Gift.get_user_gifts(uid)
    my_wishes_count = Gift.get_wishes_count(my_gifts)
    view_model = MyTrades(my_gifts, my_wishes_count)
    return render_template('my_gifts.html', gifts=view_model.trades)


@redprint.route('/<gid>/redraw')
@login_required
def redraw(gid):
    pass