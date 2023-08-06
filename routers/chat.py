from fastapi import APIRouter

from presentation.chat_controller import ChatController


router = APIRouter()


@router.get("/")
def chat():
    chat_controller = ChatController()
    return chat_controller.chat()
