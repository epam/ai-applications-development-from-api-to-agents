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
        #TODO:
        # 1. Get `api_key` from `request.headers.get("X-API-Key")`
        # 2. If `api_key != API_KEY`, return JSONResponse with:
        #       - body: {"error": "Unauthorized", "detail": "Invalid or missing API key"}
        #       - status_code=401
        # 3. Return `await call_next(request)`
        raise NotImplementedError()