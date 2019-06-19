from flask import current_app
from sqlalchemy import Column, String, Integer, Boolean

from app.libs.api import YuShuBook
from app.models.base import Base
from app.models.user import User


class Gift(Base):
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

    def is_yourself_gift(self, uid):
        if self.uid == uid:
            return True

    @staticmethod
    def recent():
        index_page = current_app.config.get('INDEX_PAGE', 30)
        gifts = Gift.query.filter_by(
            launched=False).order_by(
            Gift.create_time.desc()).distinct(Gift.isbn).limit(
            index_page).all()
        return gifts



