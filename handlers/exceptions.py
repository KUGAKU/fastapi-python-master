from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"exception": "InternalServerError", "reason": str(exc)},
    )


async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"exception": "ValidationError", "reason": exc.errors()},
    )
