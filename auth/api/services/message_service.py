from conf import get_session
from models.db import MessageModel
from models.db import User
from models.db import Chat


def create_message(text, user_id, chat_id, file=None):
    session = get_session()
    try:

        count = session.query(MessageModel).filter_by(chat_id=chat_id).order_by(MessageModel.id.asc()).count()
        if count >= 1000:
            oldest = session.query(MessageModel).filter_by(chat_id=chat_id).order_by(MessageModel.created_at).first()
            if oldest:
                session.delete(oldest)
                session.commit()

        chat = session.query(Chat).filter_by(id=chat_id).first()
        user = session.query(User).get(user_id)
        message = MessageModel(text=text, user=user, chat=chat, file=file)
        session.add(message)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()


def get_last_message():
    session = get_session()
    return session.query(MessageModel).order_by(MessageModel.id.desc()).first()


def get_all_messages(chat_id):
    session = get_session()
    return session.query(MessageModel).filter_by(chat_id=chat_id).order_by(MessageModel.id.asc()).all()

