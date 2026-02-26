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
    if not accept_header:
        return False

    accept_types = [t.strip().lower() for t in accept_header.split(',')]
    has_json = any('application/json' in t for t in accept_types)
    has_sse = any('text/event-stream' in t for t in accept_types)

    return has_json and has_sse


async def _create_sse_stream(messages: list):
    """Create Server-Sent Events stream for responses"""
    for message in messages:
        print(messages)
        event_data = f"data: {json.dumps(message.dict(exclude_none=True))}\n\n"
        yield event_data.encode('utf-8')

    yield b"data: [DONE]\n\n"


@app.post("/mcp")
async def handle_mcp_request(
        request: MCPRequest,
        response: Response,
        accept: Optional[str] = Header(None),
        mcp_session_id: Optional[str] = Header(None, alias=MCP_SESSION_ID_HEADER)
):
    """Single MCP endpoint handling all JSON-RPC requests with proper session management"""
    # Validate Accept header for all requests
    if not _validate_accept_header(accept):
        error_response = MCPResponse(
            id="server-error",
            error=ErrorResponse(
                code=-32600,
                message="Client must accept both application/json and text/event-stream"
            )
        )
        return Response(
            status_code=406,
            content=error_response.model_dump_json(),
            media_type="application/json"
        )

    # Handle initialization (no session required)
    if request.method == "initialize":
        mcp_response, session_id = mcp_server.handle_initialize(request)

        if session_id:
            response.headers[MCP_SESSION_ID_HEADER] = session_id
            mcp_session_id = session_id
    else:
        # Validate Mcp-Session-Id header presence
        if not mcp_session_id:
            error_response = MCPResponse(
                id="server-error",
                error=ErrorResponse(
                    code=-32600,
                    message="Missing session ID"
                )
            )
            return Response(
                status_code=400,
                content=error_response.model_dump_json(),
                media_type="application/json"
            )

        session = mcp_server.get_session(mcp_session_id)
        if not session:
            return Response(
                status_code=400,
                content="No valid session ID provided"
            )

        # Handle notifications that don't need responses
        if request.method == "notifications/initialized":
            session.ready_for_operation = True
            print("Client initialization complete")
            return Response(
                status_code=202,
                headers={MCP_SESSION_ID_HEADER: session.session_id},
            )

        # Handle different MCP methods
        if not session.ready_for_operation:
            error_response = MCPResponse(
                id="server-error",
                error=ErrorResponse(
                    code=-32600,
                    message="Missing session ID"
                )
            )
            return Response(
                status_code=400,
                content=error_response.model_dump_json(),
                media_type="application/json"
            )

        if request.method == "tools/list":
            mcp_response = mcp_server.handle_tools_list(request)
        elif request.method == "tools/call":
            mcp_response = await mcp_server.handle_tools_call(request)
        else:
            mcp_response = MCPResponse(
                id=request.id,
                error=ErrorResponse(
                    code=-32602,
                    message=f"Method '{request.method}' not found"
                )
            )

    return StreamingResponse(
        content=_create_sse_stream([mcp_response]),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            MCP_SESSION_ID_HEADER: mcp_session_id
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="debug"
    )
