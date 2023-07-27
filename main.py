from fastapi import FastAPI
from routers import sample, chat

app = FastAPI()

app.include_router(sample.router, prefix="/sample")
app.include_router(chat.router, prefix="/chat")
