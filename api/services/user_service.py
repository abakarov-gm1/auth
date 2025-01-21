from conf.database import get_session
from models.db.user_model import User
from sqlalchemy import null
from sqlalchemy.exc import NoResultFound
from sqlalchemy.inspection import inspect


def create_user(
        phone=None,
        name=None,
        password=None,
        region=None,
        subscription="base",
        telegram_id=None,
        telegram_username=None
):
    session = get_session()
    new_user = User(
        phone=phone,
        name=name,
        password=password,
        subscription=subscription,
        region=region,
        telegram_id=telegram_id,
        telegram_username=telegram_username
    )
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


def get_user_login_service(phone):
    session = get_session()
    return session.query(User).filter(User.phone == phone).first()


def get_user_service(user_id):
    session = get_session()
    return session.query(User).filter(User.id == user_id).first()


def put_user_service(user_id, update_data):
    update_data = update_data.dict()
    session = get_session()

    try:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if not user:
            return {"error": "User not found"}

        valid_columns = {col.key for col in inspect(User).mapper.column_attrs}
        for key, value in update_data.items():
            if value is None:
                continue
            if key in valid_columns:
                setattr(user, key, value)

        session.commit()
        session.refresh(user)
        return user

    except Exception as e:
        session.rollback()
        return {"error": str(e)}

    finally:
        session.close()


def get_balance(user_id):
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user.balance
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()


def add_balance(user_id, balance):
    balance = balance.dict()
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"message": "User not found"}
        user.balance += balance.get("balance")
        session.commit()
        session.refresh(user)
        return {"message": "success"}

    except Exception as e:
        session.rollback()
        return {"error": str(e)}

    finally:
        session.close()


def update_subscription(user_id, subscription):
    subscription = subscription.dict()
    session = get_session()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"message": "User not found"}

        key = list(subscription.keys())[0]
        setattr(user, key, subscription[key])
        session.commit()
        session.refresh(user)
        return {"message": "success"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        session.close()


def check_phone_telegram_id(user_phone, telegram_id):
    session = get_session()
    user = session.query(User).filter(User.phone == user_phone and User.telegram_id == telegram_id).first()
    if user:
        return True
    return False
