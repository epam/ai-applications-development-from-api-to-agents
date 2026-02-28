import uvicorn

from t11_mcp_auth.mcp_server._server import mcp
from t11_mcp_auth.mcp_server.auth.oauth import JWTAuthMiddleware

#TODO:
# 1. Create a Starlette app from `mcp.streamable_http_app()`, assign to `app`
# 2. Add `JWTAuthMiddleware` to the app via `app.add_middleware(JWTAuthMiddleware)`

if __name__ == "__main__":
    #TODO:
    # 3. Run uvicorn with:
    #       - app=app, host="0.0.0.0", port=8008, log_level="info"
    raise NotImplementedError()