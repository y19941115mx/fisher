from flask import current_app
from sqlalchemy import Column, String, Integer, Boolean, func

from app.libs.api import YuShuBook
from app.models.base import Base, db


class Gift(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    isbn = Column(String(13), nullable=False)
    launched = Column(Boolean, default=False)

    def __hash__(self):
        return self.isbn.__hash__()

    def __eq__(self, other):
        return self.isbn == other.isbn

    @property
    def user(self):
        from app.models.user import User
        return User.query.filter_by(id=self.uid).first()

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    def is_yourself_gift(self, uid):
        if self.uid == uid:
            return True

    @classmethod
    def recent(cls):
        index_page = current_app.config.get('INDEX_PAGE', 30)
        gifts = cls.query.filter_by(
            launched=False).order_by(
            Gift.create_time.desc()).limit(
            index_page).all()

        return set(gifts)

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = cls.query.filter_by(uid=uid, launched=False).order_by(
            cls.create_time.desc()).all()
        return gifts

    @staticmethod
    def get_wishes_count(gifts_list):
        isbn_list = [gift.isbn for gift in gifts_list]
        from app.models.wish import Wish
        wishes_count_list = db.session.query(Wish.isbn, func.count('*')).filter(
            Wish.launched == False, Wish.status == 1, Wish.isbn.in_(isbn_list)
        ).group_by(Wish.isbn).all()

        wishes_count = {item[0]: item[1] for item in wishes_count_list}
        return wishes_count






