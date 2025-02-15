from fastapi import APIRouter
from services.chat_service import create_chat_service
from schemas.chat_model import CreateChat


router = APIRouter()


@router.post("/new")
def create_new_chat(data: CreateChat):
    create_chat_service(data.name)
    return {"message": "New chat created"}

