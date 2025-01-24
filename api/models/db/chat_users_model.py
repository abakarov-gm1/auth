from models.db.base import Base
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey


class ManyToManyChats(Base):
    __tablename__ = 'chat_users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey('chat.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

