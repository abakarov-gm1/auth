from fastapi import APIRouter
from services.user_service import (get_user_service,
                                       put_user_service,
                                       get_balance,
                                       add_balance,
                                       update_subscription)
from schemas.user_model import UpdateUser, UpdateBalance, Subscription


router = APIRouter()


@router.get("/profile")
def get_user(user_id: int):
    return get_user_service(user_id)


@router.put('/profile')
def put_user(user_id: int, update_data: UpdateUser):
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




