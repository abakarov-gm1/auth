from conf.database import get_session
from models.db.user_model import User


def create_user(name, password, balance, subscription):
    session = get_session()
    new_user = User(name=name, password=password, balance=balance, subscription=subscription)
    session.add(new_user)
    session.commit()
    session.close()


