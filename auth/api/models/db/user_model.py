from sqlalchemy.orm import relationship

from .base import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    phone = Column(String, nullable=True, unique=True)
    is_verified = Column(Boolean, default=False)
    telegram_id = Column(String, nullable=True, unique=True)
    telegram_username = Column(String, nullable=True, unique=True)
    balance = Column(Integer, nullable=False, default=0)  # баланс
    subscription = Column(String, nullable=True)  # уровни подписок
    region = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    role = Column(String, default="user")

    chats = relationship('Chat', secondary="chat_users",  back_populates="users")
    message = relationship("MessageModel", back_populates="user")

