from sqlalchemy import Column, String, Boolean, Float, Integer

from app.models import Base
from flask_login import UserMixin
from app.ext import login_manager


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    password = Column(String(100), nullable=False)
    # 用户是否激活
    confirmed = Column(Boolean, default=False)

@login_manager.user_loader
def user_loader(id):
    return User.get_id(id)