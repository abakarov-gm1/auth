from .base import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    is_verified = Column(Boolean, default=False)
    telegram_id = Column(String, nullable=True)
    balance = Column(Integer, nullable=False, default=0)  # баланс
    subscription = Column(String, nullable=False)  # уровни подписок
    region = Column(String, nullable=True)

    # history_smet = /

