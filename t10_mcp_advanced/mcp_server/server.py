import json
from typing import Optional

import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import Response
from fastapi.responses import StreamingResponse

from models.request import MCPRequest
from t10_mcp_advanced.mcp_server.models.response import MCPResponse, ErrorResponse
from t10_mcp_advanced.mcp_server.ums_mcp_server import UmsMCPServer

MCP_SESSION_ID_HEADER = "Mcp-Session-Id"

# FastAPI app
app = FastAPI(title="MCP Tools Server", version="1.0.0")
mcp_server = UmsMCPServer()


def _validate_accept_header(accept_header: Optional[str]) -> bool:
    """Validate that client accepts both JSON and SSE"""
    #TODO:
    # 1. Check if `accept_header` is None or falsy, return False if so
    # 2. Split `accept_header` by commas and create `accept_types` list with stripped and lowercased values
    # 3. Check if any type in `accept_types` contains 'application/json' and assign to `has_json`
    # 4. Check if any type in `accept_types` contains 'text/event-stream' and assign to `has_sse`
    # 5. Return `has_json and has_sse`
    raise NotImplementedError()

async def _create_sse_stream(messages: list):
    """Create Server-Sent Events stream for responses"""
    #TODO:
    # 1. Iterate through `messages` list
    # 2. For each message, create `event_data` string in format: f"data: {json.dumps(message.dict(exclude_none=True))}\n\n"
    # 3. Yield `event_data.encode('utf-8')`
    # 4. After loop, yield final message: b"data: [DONE]\n\n" (indicator that the streaming is finished)
    raise NotImplementedError()

@app.post("/mcp")
async def handle_mcp_request(
        request: MCPRequest,
        response: Response,
        accept: Optional[str] = Header(None),
        mcp_session_id: Optional[str] = Header(None, alias=MCP_SESSION_ID_HEADER)
):
    """Single MCP endpoint handling all JSON-RPC requests with proper session management"""
    #TODO:
    # 1. Validate Accept header:
    #       - Call `_validate_accept_header(accept)`
    #       - If False, create `error_response` with MCPResponse:
    #           - id="server-error",
    #           - error=ErrorResponse(code=-32600, message="Client must accept both application/json and text/event-stream")
    #       - Return Response with:
    #           - status_code=406,
    #           - content=error_response.model_dump_json(),
    #           - media_type="application/json"
    # 2. Handle initialization (no session required):
    #       - If `request.method == "initialize"`:
    #           - Call `mcp_server.handle_initialize(request)` and assign to `mcp_response, session_id`
    #           - If `session_id` exists, set `response.headers[MCP_SESSION_ID_HEADER] = session_id` and `mcp_session_id = session_id`
    # 3. Handle other methods (session required):
    #       - Else block for non-initialize methods:
    #           - Validate `mcp_session_id` exists, if not create error_response with
    #               MCPResponse(id="server-error", error=ErrorResponse(code=-32600, message="Missing session ID"))
    #               and return Response with:
    #                   - status_code=400
    #                   - content=error_response.model_dump_json()
    #                   - media_type="application/json"
    #           - Get `session` from `mcp_server.get_session(mcp_session_id)`
    #           - If no session, return Response with:
    #               - status_code=400
    #               - content="No valid session ID provided"
    #           - Handle notifications/initialized: if `request.method == "notifications/initialized"` then set
    #               - `session.ready_for_operation = True`
    #               - then return Response with status_code=202 and headers={MCP_SESSION_ID_HEADER: session.session_id}
    #           - Check if session is ready:
    #               - if not `session.ready_for_operation`, then create error_response and return Response with status_code=400
    #                   and MCPResponse(id="server-error", error=ErrorResponse(code=-32600, message="Missing session ID"))
    #           - Handle tools/list: if `request.method == "tools/list"`, call `mcp_server.handle_tools_list(request)` and assign to `mcp_response`
    #           - Handle tools/call: if `request.method == "tools/call"`, call `mcp_server.handle_tools_call(request)` and assign to `mcp_response`
    #           - Handle unknown methods: else create `mcp_response` with MCPResponse(id=request.id, error=ErrorResponse(code=-32602, message=f"Method '{request.method}' not found"))
    # 4. Return StreamingResponse:
    #       - content=_create_sse_stream([mcp_response])
    #       - media_type="text/event-stream"
    #       - headers={"Cache-Control": "no-cache", "Connection": "keep-alive", MCP_SESSION_ID_HEADER: mcp_session_id}
    raise NotImplementedError()

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="debug"
    )
