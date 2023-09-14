from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    def exist_auth_header(self, auth_header: str | None) -> bool:
        if auth_header:
            return True
        return False

    def is_preflight_request(self, request: Request) -> bool:
        if request.method == "OPTIONS":
            return True
        return False

    def is_swagger_docs_request(self, request: Request) -> bool:
        path = request.url.path.split("/")[-1]
        if path == "docs":
            return True
        if path == "openapi.json":
            return True
        return False

    async def dispatch(self, request: Request, call_next):
        if self.is_swagger_docs_request(request):
            response = await call_next(request)
            return response

        if self.is_preflight_request(request):
            response = await call_next(request)
            return response

        auth_header = request.headers.get("Authorization")
        if not self.exist_auth_header(auth_header):
            raise HTTPException(
                status_code=401, detail="Authorization header is not found"
            )
        access_token = None
        try:
            token_type, token_value = auth_header.split(" ")
            if token_type == "Bearer":
                access_token = token_value
        except ValueError:
            raise HTTPException(
                status_code=401, detail="Invalid Authorization header format"
            )

        response = await call_next(request)

        return response
