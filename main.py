from fastapi import FastAPI
from routers import sample, echo

app = FastAPI()

app.include_router(sample.router, prefix="/sample")
app.include_router(echo.router, prefix="/echo")



