from conf import get_session
from models.db import Chat
from models.db import User


def create_chat_service(name):
    session = get_session()
    try:
        new_chat = Chat(name=name)
        session.add(new_chat)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()


# можно сделать что бы сразу добавились только пользователи у которых есть подписка


def add_users_to_chat_service(chat_id, user_id):
    session = get_session()
    chat = session.query(Chat).filter_by(id=chat_id).first()
    user = session.query(User).filter_by(id=user_id).first()
    chat.users.append(user)
    session.commit()


def get_users_from_chat_service(chat_id):
    session = get_session()
    chat = session.query(Chat).filter_by(id=chat_id).first()
    users = chat.users
    return users


# def get_chat_service(chat_id):
#     session = get_session()
#     session = session.query(Chat).filter_by(id=chat_id).first()
#
