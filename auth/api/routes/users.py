import os
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form
from repositories.user_repository import (get_user_service,
                                       put_user_service,
                                       get_balance,
                                       add_balance,
                                       update_subscription)
from schemas.user_model import UpdateUser, UpdateBalance, Subscription

from conf import UPLOAD_DIR

router = APIRouter()


@router.get("/profile")
def get_user(token: str):
    return get_user_service(token)


@router.put('/profile')
def put_user(
        user_id: int,
        name: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        balance: Optional[int] = Form(None),
        region: Optional[str] = Form(None),
        photo: Optional[UploadFile] = File(None)
):
    photo_path = None
    if photo is not None:
        photo_path = os.path.join(UPLOAD_DIR, photo.filename)
        with open(photo_path, "wb") as buffer:
            buffer.write(photo.file.read())

    update_data = {"name": name, "phone": phone, "balance": balance, "region": region, "photo": photo_path}
    return put_user_service(user_id, update_data)


@router.get('/profile/balance')
def get_user_balance(user_id: int):
    return get_balance(user_id)


@router.post('profile/balance/recharge')
def add_user_balance(user_id: int, data: UpdateBalance):
    return add_balance(user_id, data)


@router.put("/profile/subscription")
def put_user_subscription(user_id: int, data: Subscription):
    return update_subscription(user_id, data)




