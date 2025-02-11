from controllers.auth.veryfy_phone import send_sms
from repositories.user_repository import reset_password_service
from controllers.auth.registry import hash_password


def reset_passwd(data):
    data = data.dict()
    send_sms(data.phone)
    if data['new_password'] != data['confirm_password']:
        return {"message": "пароли не совпадают"}

    new_password = hash_password(data['new_password'])
    return reset_password_service(data["phone"], new_password)
