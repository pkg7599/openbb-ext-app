import hashlib

from fastapi import Request
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    SECRET_TOKEN = "openbb-ext-app-v1"

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public routes
        if request.base_url.hostname in [
            "localhost",
            "127.0.0.1",
        ] or request.url.path in ["/docs", "/openapi.json", "/health"]:
            return await call_next(request)

        # Extract token
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"},
            )

        # Expecting: Authorization: Bearer <token>
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid scheme")
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid Authorization header format"},
            )

        # Validate token
        if token != self.hash_token(self.SECRET_TOKEN):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid API token"},
            )

        # Continue request
        response = await call_next(request)
        return response
