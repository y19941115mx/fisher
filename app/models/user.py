import math

from sqlalchemy import Column, String, Boolean, Float, Integer, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.token import generate_token, translate_token
from app.libs.util import is_isbn_or_key
from app.models import Base, db
from flask_login import UserMixin
from app.ext import login_manager
from app.libs.api import YuShuBook


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False, unique=True)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    _password = Column('password', String(100), nullable=False)
    # 用户是否激活
    confirmed = Column(Boolean, default=False)

    @orm.reconstructor
    def __init__(self):
        super(User, self).__init__()
        self.fields = ['id', 'nickname', 'phone_number']

    @property
    def is_active(self):
        return self.confirmed

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def generate_token(self, expiration=None):
        data = {'id': self.id}
        return generate_token(data, expiration)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def confirm_token(token):
        data = translate_token(token)
        if not data:
            return False
        uid = data.get('id')
        user = User.query.filter_by(id=uid).first()
        if user:
            user.confirmed = True
            db.session.commit()
            return True
        return False

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        from app.models.gift import Gift
        from app.models.wish import Wish

        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def is_in_gifts(self, isbn):
        from app.models.gift import Gift
        return True if Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False
                                            ).first() else False

    def is_in_wishes(self, isbn):
        from app.models.wish import Wish
        return True if Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False
                                            ).first() else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    def can_satisfied_wish(self):
        # 鱼豆不足
        if self.beans < 1:
            return False
        # 每索取两本书 自己必须送出一本书
        return True if math.floor(self.receive_counter / 2) <= self.send_counter else False


@login_manager.user_loader
def user_loader(uid):
    return User.query.filter_by(id=uid).first()
