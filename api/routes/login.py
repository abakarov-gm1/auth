from fastapi import APIRouter
from models.pydentic.auth_model import Login
from use_cases.auth.login import login_case


router = APIRouter()


@router.post("/login")
def login(data: Login):
    return login_case(data)

