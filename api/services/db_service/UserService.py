from conf.database import get_session
from models.db.user_model import User


def create_user(name, password, subscription):
    session = get_session()
    new_user = User(name=name, password=password, subscription=subscription)
    session.add(new_user)
    session.commit()
    session.close()


def update_status(phone):
    session = get_session()
    try:
        user = session.query(User).filter(User.phone == phone).first()

        if user is None:
            print(f"Пользователь с номером {phone} не найден.")
            return
        user.is_verified = 1
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при обновлении данных: {e}")
    finally:
        session.close()

