from t9_mcp_fundamentals.mcp_server._server import mcp

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )