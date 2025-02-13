import os
from controllers.auth.login import pwd_context
from controllers.auth.veryfy_phone import send_sms
from repositories.user_repository import get_user_login_service, create_user
from conf import UPLOAD_DIR


os.makedirs(UPLOAD_DIR, exist_ok=True)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def registry_cases(phone, name, password, region, photo):
    if get_user_login_service(phone):
        return {"message": "номер уже зарегестрирован !"}
    password = hash_password(password)

    photo_path = None
    if photo:
        photo_path = os.path.join(UPLOAD_DIR, photo.filename)
        with open(photo_path, "wb") as buffer:
            buffer.write(photo.file.read())

    create_user(phone=phone, name=name, password=password, region=region, photo=photo_path)
    send_sms(phone)
    return {"message": "success"}





