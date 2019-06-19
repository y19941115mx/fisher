from app.libs.redprint import Redprint
from flask_login import login_required, current_user
from flask import redirect, url_for, flash, render_template

from app.models import db
from app.models.wish import Wish
from app.view_models.trade import MyTrades

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


@redprint.route('/my/wishes')
@login_required
def my_wishes():
    uid = current_user.id
    my_wishes = Wish.get_user_wishes(uid)
    my_wishes_count = Wish.get_gifts_count(my_wishes)
    view_model = MyTrades(my_wishes, my_wishes_count)
    return render_template('my_wish.html', wishes=view_model.trades)


@redprint.route('/satisfy/<int:wid>')
def satisfy_wish(wid):
    return 'hello'


@redprint.route('/redraw/wid')
@login_required
def redraw(wid):
    pass
