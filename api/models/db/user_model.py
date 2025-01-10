from .base import Base
from sqlalchemy import Column, Integer, String


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Integer, default=0)
    balance = Column(Integer, nullable=False, default=0)  # баланс
    subscription = Column(String, nullable=False)  # уровни подписок


