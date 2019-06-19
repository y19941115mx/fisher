from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from app.libs.api import YuShuBook
from app.models import Base
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
        return yushu_book
