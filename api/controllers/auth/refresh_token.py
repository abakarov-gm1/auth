import os

import redis
from conf.redis import redis_connection
from controllers.auth.login import create_access_token, create_refresh_token
from jose import jwt


SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        return {"error": str(e)}


def refresh(data):
    user_id = data.user_id
    access_token = data.access_token
    refresh_token = data.refresh_token

    redis_key = f"refresh_token:{user_id}"
    stored_refresh_token = redis_connection().get(redis_key)

    if not stored_refresh_token:
        return {"error": "Refresh token not found"}

    last_six = access_token[-6:]
    if not refresh_token.endswith(last_six) or stored_refresh_token != refresh_token:
        return {"error": "Invalid refresh token"}

    new_access_token = create_access_token({"user_id": user_id})
    new_refresh_token = create_refresh_token(new_access_token, user_id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }












