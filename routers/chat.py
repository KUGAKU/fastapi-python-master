from fastapi import APIRouter
from injector import Injector
from di_modules.chat_di import ChatDi

from presentation.chat_controller import ChatController


router = APIRouter()


@router.get("/")
def chat(chatMessage: str):
    injector = Injector([ChatDi()])
    chat_controller = injector.get(ChatController)
    return chat_controller.start(chatMessage)
