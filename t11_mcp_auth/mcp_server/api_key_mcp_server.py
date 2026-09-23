import uvicorn

from t11_mcp_auth.mcp_server._server import mcp
from t11_mcp_auth.mcp_server.auth.api_key_auth import APIKeyMiddleware

# Stateless Streamable HTTP app: no sessions, every request is authenticated and processed on its own
app = mcp.http_app(stateless_http=True)
app.add_middleware(APIKeyMiddleware)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8007,
        log_level="info"
    )
