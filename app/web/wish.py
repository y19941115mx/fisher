from app.libs.redprint import Redprint
from flask_login import login_required, current_user
from flask import redirect, url_for, flash, render_template, abort

from app.libs.util import send_email
from app.models import db
from app.models.gift import Gift
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


@redprint.route('/<int:wid>/satisfy')
@login_required
def satisfy_wish(wid):
    """
            向想要这本书的人发送一封邮件
            注意，这个接口需要做一定的频率限制
            这接口比较适合写成一个ajax接口
        """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_email(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book:detail', isbn=wish.isbn))


@redprint.route('/<wid>/redraw')
@login_required
def redraw(wid):
    wish = Wish.query.filter_by(id=wid).first_or_404()

    with db.auto_commit():
        wish.status = 0

    return redirect(url_for('web.wish:my_wish'))
