from sqlalchemy import Column, Integer, String, Boolean, Text, orm, Float

from app.models import Base


class Healthy(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    alarm_msg = Column(Text)
    heart_rate = Column(Integer, nullable=False)
    blood_pressure = Column(String(30), nullable=False)# 高血压/低血压
    blood_sugar = Column(Float, nullable=False)

    @orm.reconstructor
    def __init__(self):
        super(Healthy, self).__init__()
        self.fields = ['alarm_msg', 'heart_rate', 'blood_pressure', 'blood_sugar']

class Notice(Base):
    id = Column(Integer, primary_key=True)
    msg = Column(Text)

    @orm.reconstructor
    def __init__(self):
        super(Notice, self).__init__()
        self.fields = ['msg']


class Article(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    msg = Column(Text)

    @orm.reconstructor
    def __init__(self):
        super(Article, self).__init__()
        self.fields = ['id', 'nickname', 'phone_number']






