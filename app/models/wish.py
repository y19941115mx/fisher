from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, func
from sqlalchemy.orm import relationship

from app.libs.api import YuShuBook
from app.models import Base, db
from app.models.user import User


class Wish(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    isbn = Column(String(13), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def user(self):
        return User.query.filter_by(id=self.uid).first()

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = cls.query.filter_by(uid=uid, launched=False).order_by(
            cls.create_time.desc()).all()
        return wishes

    @staticmethod
    def get_gifts_count(wishes_list):
        isbn_list = [wish.isbn for wish in wishes_list]
        from app.models.gift import Gift
        gifts_count_list = db.session.query(Gift.isbn, func.count('*')).filter(
            Gift.launched == False, Gift.status == 1, Gift.isbn.in_(isbn_list)
        ).group_by(Gift.isbn).all()

        gifts_count = {item[0]: item[1] for item in gifts_count_list}
        return gifts_count
