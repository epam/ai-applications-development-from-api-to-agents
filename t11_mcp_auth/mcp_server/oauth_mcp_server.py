import uvicorn

from t11_mcp_auth.mcp_server._server import mcp
from t11_mcp_auth.mcp_server.auth.oauth import JWTAuthMiddleware

#TODO:
# 1. Create a stateless Starlette app from `mcp.http_app(stateless_http=True)`, assign to `app`
#    (no sessions: every request is authenticated and processed on its own)
# 2. Add `JWTAuthMiddleware` to the app via `app.add_middleware(JWTAuthMiddleware)`

if __name__ == "__main__":
    #TODO:
    # 3. Run uvicorn with:
    #       - app=app, host="0.0.0.0", port=8008, log_level="info"
    raise NotImplementedError()