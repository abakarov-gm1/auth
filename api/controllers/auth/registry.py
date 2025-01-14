from controllers.auth.login import pwd_context
from controllers.auth.veryfy_phone import send_sms
from services.user_service import get_user, create_user


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def registry_cases(data):
    if get_user(data.phone):
        return {"message": "номер уже зарегестрирован !"}
    password = hash_password(data.password)
    create_user(data.phone, data.name, password, data.region)
    send_sms(data.phone)
    return {"message": "success"}





