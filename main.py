from fastapi import FastAPI
from pydantic import ValidationError
from handlers.exceptions import validation_error_handler
from middleware.auth_middleware import AuthMiddleware
from routers import sample, chat
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS設定のリストを定義します
origins = [
    "http://localhost:3000",  # ローカルのNuxt.jsアプリのURL
    "https://thankful-mud-055bfe800.3.azurestaticapps.net",
]

# MiddlewareにCORSを追加します
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 上で定義したオリジンのリストを設定します
    allow_methods=["*"],  # すべてのHTTPメソッドを許可します
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可します
)

app.add_middleware(AuthMiddleware)

app.add_exception_handler(ValidationError, validation_error_handler)


app.include_router(sample.router, prefix="/sample")
app.include_router(chat.router, prefix="/chat")
