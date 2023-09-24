from typing import Optional
from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from injector import Injector
from di_modules.chat_di import ChatDi

from presentation.chat_controller import ChatController
from schemas.chat import ChatRequest


router = APIRouter()

security = HTTPBearer()


@router.post("/")
def chat(request: ChatRequest, _: HTTPAuthorizationCredentials = Security(security)):
    injector = Injector([ChatDi()])
    chat_controller = injector.get(ChatController)
    return chat_controller.startChat(request.chat_message, request.conversation_id)
