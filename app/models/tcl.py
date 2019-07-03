from sqlalchemy import Column, Integer, String, Boolean, Text

from app.models import Base


class Healthy(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    alarm_msg = Column(Text)
    heart_rate = Column(Integer, nullable=False)
    blood_pressure = Column(Integer, nullable=False)
    blood_sugar = Column(Integer, nullable=False)


class Notice(Base):
    id = Column(Integer, primary_key=True)
    msg = Column(Text)


class Article(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    msg = Column(Text)






