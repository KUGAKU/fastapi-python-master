from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"exception": "ValidationError", "reason": exc.errors()},
    )
