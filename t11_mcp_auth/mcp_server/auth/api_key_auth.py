from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

API_KEY: str = "dev-secret-key"


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware that validates the X-API-Key header on every
    incoming request before it reaches the MCP server.
    """

    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            return JSONResponse(
                {"error": "Unauthorized", "detail": "Invalid or missing API key"},
                status_code=401
            )
        return await call_next(request)
