from typing import Optional
from fastapi import APIRouter
from injector import Injector
from di_modules.chat_di import ChatDi

from presentation.chat_controller import ChatController
from schemas.chat import ChatRequest


router = APIRouter()


@router.post("/")
def chat(request: ChatRequest):
    injector = Injector([ChatDi()])
    chat_controller = injector.get(ChatController)
    return chat_controller.startChat(request.chat_message, request.conversation_id)
