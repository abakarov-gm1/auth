from conf.database import get_session
from models.db.user_model import User


def create_user(phone, name, password, region, subscription="base"):
    session = get_session()
    new_user = User(phone=phone, name=name, password=password, subscription=subscription, region=region)
    session.add(new_user)
    session.commit()
    session.close()


def update_status(phone):
    flag = False
    session = get_session()
    try:
        user = session.query(User).filter(User.phone == phone).first()

        if user is None:
            print(f"Пользователь с номером {phone} не найден.")
            return
        user.is_verified = True
        session.commit()
        flag = True
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении данных: {e}")
    finally:
        session.close()
        return flag


def get_user(phone):
    session = get_session()
    return session.query(User).filter(User.phone == phone).first()


