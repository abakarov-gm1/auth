from services.db_service.UserService import get_user, create_user
from use_cases.auth.login import pwd_context
from use_cases.auth.veryfy_phone import send_sms


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def registry_cases(data):
    if get_user(data.phone):
        return {"message": "номер уже зарегестрирован !"}
    password = hash_password(data.password)
    create_user(data.phone, data.name, password, data.region)
    send_sms(data.phone)
    return {"message": "success"}





