import os
from datetime import datetime, timedelta

from passlib.context import CryptContext

from models.pydentic.auth_model import Login
from services.db_service.UserService import get_user
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Устанавливаем время истечения токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def login_case(data: Login):
    user = get_user(data.phone)
    if not user:
        return {"message": "user is not found"}

    if not verify_password(data.password, user.password):
        return {"message": "password or phone not verify"}

    if not user.is_verified:
        return {"message": "phone is not verified"}

    access_token = create_access_token(data={"user_id": user.id})
    return {"token": access_token}
