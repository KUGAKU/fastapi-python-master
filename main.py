from fastapi import FastAPI
from middleware.auth_middleware import AuthMiddleware
from routers import sample, chat
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS設定のリストを定義します
origins = [
    "http://localhost:3000",  # ローカルのNuxt.jsアプリのURL
]

# MiddlewareにCORSを追加します
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 上で定義したオリジンのリストを設定します
    allow_methods=["*"],  # すべてのHTTPメソッドを許可します
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可します
)

app.add_middleware(AuthMiddleware)

app.include_router(sample.router, prefix="/sample")
app.include_router(chat.router, prefix="/chat")
