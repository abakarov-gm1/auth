from datetime import datetime

from sqlalchemy.orm import relationship

from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, BigInteger, ForeignKey, DateTime


class MessageModel(Base):
    __tablename__ = 'message'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    file = Column(String, nullable=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    recipient_id = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="message")





