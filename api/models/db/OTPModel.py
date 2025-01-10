import datetime
from xmlrpc.client import DateTime

from database import Base
from sqlalchemy import Column, Integer, String


class Otp(Base):

    __tablename__ = 'otp'

    id = Column(Integer, primary_key=True)
    phone = Column(String)
    sms_code = Column(String)
    create_data = Column(DateTime, default=datetime.datetime.utcnow())
    expires_data = Column(DateTime, default=lambda: datetime.datetime.utcnow() - datetime.timedelta(5))



