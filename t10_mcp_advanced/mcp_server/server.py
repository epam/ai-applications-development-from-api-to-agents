import base64
import json
from typing import Optional
from urllib.parse import urlparse

import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import Response
from fastapi.responses import StreamingResponse

from models.request import MCPRequest
from t10_mcp_advanced.mcp_server.models.response import MCPResponse, ErrorResponse
from t10_mcp_advanced.mcp_server.ums_mcp_server import UmsMCPServer, PROTOCOL_VERSION_META_KEY

# Streamable HTTP request headers (https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
MCP_PROTOCOL_VERSION_HEADER = "MCP-Protocol-Version"
MCP_METHOD_HEADER = "Mcp-Method"
MCP_NAME_HEADER = "Mcp-Name"

HEADER_MISMATCH_ERROR_CODE = -32020
ALLOWED_ORIGIN_HOSTS = {"localhost", "127.0.0.1"}

# FastAPI app
app = FastAPI(title="MCP Tools Server", version="1.0.0")
mcp_server = UmsMCPServer()


def _validate_origin(origin: Optional[str]) -> bool:
    """Protect against DNS rebinding: requests from a browser must come from a local origin"""
    if not origin:
        return True
    return urlparse(origin).hostname in ALLOWED_ORIGIN_HOSTS


def _validate_accept_header(accept_header: Optional[str]) -> bool:
    """Validate that client accepts both JSON and SSE"""
    #TODO:
    # 1. Check if `accept_header` is None or falsy, return False if so
    # 2. Split `accept_header` by commas and create `accept_types` list with stripped and lowercased values
    # 3. Check if any type in `accept_types` contains 'application/json' and assign to `has_json`
    # 4. Check if any type in `accept_types` contains 'text/event-stream' and assign to `has_sse`
    # 5. Return `has_json and has_sse`
    raise NotImplementedError()


def _decode_header_value(value: str) -> str:
    """Values that are not plain ASCII are sent as `=?base64?{value}?=`"""
    if value.startswith("=?base64?") and value.endswith("?="):
        return base64.b64decode(value[len("=?base64?"):-len("?=")]).decode("utf-8")
    return value


def _validate_request_headers(
        request: MCPRequest,
        protocol_version: Optional[str],
        mcp_method: Optional[str],
        mcp_name: Optional[str]
) -> Optional[str]:
    """Headers mirror the request body so that proxies can route without parsing it. They must match the body"""
    #TODO:
    # Returns error message if headers don't match the request body, otherwise None
    # 1. Get protocol version from the body: `request.params["_meta"][PROTOCOL_VERSION_META_KEY]` and assign to `body_protocol_version`
    # 2. If `protocol_version != body_protocol_version` return
    #    f"{MCP_PROTOCOL_VERSION_HEADER} header value '{protocol_version}' does not match body value '{body_protocol_version}'"
    # 3. If `mcp_method != request.method` return
    #    f"{MCP_METHOD_HEADER} header value '{mcp_method}' does not match body value '{request.method}'"
    # 4. If `request.method == "tools/call"`:
    #       - Get `body_name` from `request.params.get("name")`
    #       - In try block decode header: `header_name = _decode_header_value(mcp_name) if mcp_name else None`
    #         Catch ValueError and return f"{MCP_NAME_HEADER} header value '{mcp_name}' is not valid base64"
    #       - If `header_name != body_name` return
    #         f"{MCP_NAME_HEADER} header value '{header_name}' does not match body value '{body_name}'"
    # 5. Return None
    raise NotImplementedError()


def _json_error_response(status_code: int, mcp_response: MCPResponse) -> Response:
    return Response(
        status_code=status_code,
        content=mcp_response.model_dump_json(exclude_none=True),
        media_type="application/json"
    )


async def _create_sse_stream(messages: list):
    """Create Server-Sent Events stream for responses"""
    #TODO:
    # 1. Iterate through `messages` list
    # 2. For each message, create `event_data` string in format:
    #    f"event: message\ndata: {json.dumps(message.model_dump(exclude_none=True))}\n\n"
    # 3. Yield `event_data.encode('utf-8')`
    raise NotImplementedError()


@app.post("/mcp")
async def handle_mcp_request(
        request: MCPRequest,
        accept: Optional[str] = Header(None),
        origin: Optional[str] = Header(None),
        protocol_version: Optional[str] = Header(None, alias=MCP_PROTOCOL_VERSION_HEADER),
        mcp_method: Optional[str] = Header(None, alias=MCP_METHOD_HEADER),
        mcp_name: Optional[str] = Header(None, alias=MCP_NAME_HEADER)
):
    """Single stateless MCP endpoint: every request is validated and processed on its own"""
    #TODO:
    # 1. Validate Origin header:
    #       - If `_validate_origin(origin)` is False, return `_json_error_response` with:
    #           - status_code=403
    #           - mcp_response=MCPResponse(error=ErrorResponse(code=-32600, message=f"Origin '{origin}' is not allowed"))
    # 2. Validate Accept header:
    #       - If `_validate_accept_header(accept)` is False, return `_json_error_response` with:
    #           - status_code=406
    #           - mcp_response=MCPResponse(id=request.id, error=ErrorResponse(code=-32600, message="Client must accept both application/json and text/event-stream"))
    # 3. Notifications (`request.id is None`) don't get a response: return Response(status_code=202)
    # 4. Legacy clients start with `initialize` handshake that was removed in 2026-07-28:
    #       - If `request.method == "initialize"`, return `_json_error_response` with:
    #           - status_code=400
    #           - mcp_response=mcp_server.handle_legacy_initialize(request)
    # 5. Validate `_meta`:
    #       - If `error_response := mcp_server.validate_request_meta(request)`, return `_json_error_response` with status_code=400 and `error_response`
    # 6. Validate headers:
    #       - If `mismatch := _validate_request_headers(request, protocol_version, mcp_method, mcp_name)`, return `_json_error_response` with:
    #           - status_code=400
    #           - mcp_response=MCPResponse(id=request.id, error=ErrorResponse(code=HEADER_MISMATCH_ERROR_CODE, message=mismatch))
    # 7. Handle MCP methods and assign result to `mcp_response`:
    #       - "server/discover" -> `mcp_server.handle_discover(request)`
    #       - "tools/list" -> `mcp_server.handle_tools_list(request)`
    #       - "tools/call" -> `await mcp_server.handle_tools_call(request)`
    #       - otherwise return `_json_error_response` with:
    #           - status_code=404
    #           - mcp_response=MCPResponse(id=request.id, error=ErrorResponse(code=-32601, message=f"Method '{request.method}' not found"))
    # 8. Return StreamingResponse:
    #       - content=_create_sse_stream([mcp_response])
    #       - media_type="text/event-stream"
    #       - headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    raise NotImplementedError()


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="debug"
    )
