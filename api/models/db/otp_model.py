from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, DateTime
from .base import Base


class Otp(Base):
    __tablename__ = 'otp'

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    otp = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=1))
