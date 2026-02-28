import uvicorn

from t11_mcp_auth.mcp_server._server import mcp
from t11_mcp_auth.mcp_server.auth.api_key_auth import APIKeyMiddleware

#TODO:
# 1. Create a Starlette app from `mcp.streamable_http_app()`, assign to `app`
# 2. Add `APIKeyMiddleware` to the app via `app.add_middleware(APIKeyMiddleware)`

if __name__ == "__main__":
    #TODO:
    # 3. Run uvicorn with:
    #       - app=app, host="0.0.0.0", port=8007, log_level="info"
    raise NotImplementedError()