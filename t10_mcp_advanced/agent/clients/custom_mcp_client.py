import base64
import json
import uuid
from typing import Optional, Any
import aiohttp


PROTOCOL_VERSION = "2026-07-28"
CLIENT_INFO = {
    "name": "my-custom-mcp-client",
    "version": "1.0.0"
}

class CustomMCPClient:
    """Pure Python MCP client without external MCP libraries (stateless MCP, protocol version 2026-07-28)"""

    def __init__(self, mcp_server_url: str) -> None:
        self.server_url = mcp_server_url
        self.http_session: Optional[aiohttp.ClientSession] = None

    @classmethod
    async def create(cls, mcp_server_url: str) -> 'CustomMCPClient':
        """Async factory method to create and connect CustomMCPClient"""
        instance = cls(mcp_server_url)
        await instance.connect()
        return instance

    @staticmethod
    def _encode_header_value(value: str) -> str:
        """Header values must be plain visible ASCII, otherwise they are sent as `=?base64?{value}?=`"""
        is_plain_ascii = value.isascii() and value.isprintable() and value == value.strip()
        looks_like_base64_sentinel = value.startswith("=?base64?") and value.endswith("?=")
        if is_plain_ascii and not looks_like_base64_sentinel:
            return value
        return f"=?base64?{base64.b64encode(value.encode('utf-8')).decode('ascii')}?="

    async def _send_request(self, method: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """Send JSON-RPC request to MCP server"""
        #TODO:
        # 1. Check if `self.http_session` is None, raise RuntimeError("HTTP session not initialized") if so
        # 2. Create `request_data` dictionary with:
        #       - "jsonrpc": "2.0"
        #       - "id": str(uuid.uuid4())
        #       - "method": method
        #       - "params": {
        #             **(params or {}),
        #             "_meta": {
        #                 "io.modelcontextprotocol/protocolVersion": PROTOCOL_VERSION,
        #                 "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
        #                 "io.modelcontextprotocol/clientCapabilities": {}
        #             }
        #         }
        #    There is no session, so every request carries protocol version, client info and capabilities in `_meta`
        # 3. Create `headers` dictionary with:
        #       - "Content-Type": "application/json"
        #       - "Accept": "application/json, text/event-stream" (pay attention that here is 2 Accepted content types)
        #       - "MCP-Protocol-Version": PROTOCOL_VERSION
        #       - "Mcp-Method": method
        # 4. If `method == "tools/call"`, add `headers["Mcp-Name"] = self._encode_header_value(params["name"])`
        # 5. Make async POST request using `self.http_session.post()` as `response` with:
        #       - url: self.server_url
        #       - json: request_data
        #       - headers: headers
        #    And:
        #       - Get `content_type` from `response.headers.get('content-type', '').lower()`
        #       - If `'text/event-stream' in content_type`:
        #           - call `await self._parse_sse_response_streaming(response)` and assign to `response_data`
        #       - Elif `'application/json' in content_type`:
        #           - call `await response.json()` and assign to `response_data` (errors with 4xx status are also JSON)
        #       - Otherwise raise RuntimeError(f"Unexpected response (HTTP {response.status}): {await response.text()}")
        #       - If "error" in `response_data`, extract `error = response_data["error"]` and raise RuntimeError(f"MCP Error {error['code']}: {error['message']}")
        #       - Get `result_type` from `response_data["result"].get("resultType", "complete")`
        #         If `result_type != "complete"` raise RuntimeError(f"Unsupported resultType: {result_type}")
        #         (`input_required` results of Multi Round-Trip Requests are not supported by this client)
        #       - Return `response_data`
        raise NotImplementedError()

    async def _parse_sse_response_streaming(self, response: aiohttp.ClientResponse) -> dict[str, Any]:
        """Parse Server-Sent Events response with streaming"""
        #TODO:
        # Response stream sample:
        # event: message
        # data: {"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": "some tool call result"}], "resultType": "complete"}}
        # ---
        # 1. Make async loop from the `response.content`
        #       - create `line_str` from `line.decode('utf-8').strip()`
        #       - if line doesn't start with 'data:' skip iteration (with continue). This skips empty lines, comments (`:`) and `event:` lines
        #       - extract data part: `data_part = line_str[5:].strip()` (remove 'data:' prefix), if it is empty skip iteration
        #       - in try block parse it: `message = json.loads(data_part)`, on json.JSONDecodeError skip iteration
        #       - if "id" in `message`, return `message`. The server may send notifications (e.g. progress) before
        #         the final response, only the response has `id`
        # 2. raise RuntimeError("No JSON-RPC response found in SSE stream")
        raise NotImplementedError()

    async def connect(self) -> None:
        """Create HTTP session and discover MCP server (no handshake and no session in stateless MCP)"""
        #TODO:
        # 1. Set up aiohttp.ClientTimeout with `total=30, connect=10`
        # 2. Set up aiohttp.TCPConnector with `limit=100, limit_per_host=10`
        # 3. Set up HTTP session: `self.http_session = aiohttp.ClientSession(timeout=timeout, connector=connector)`
        # 4. Try-except block:
        #       - Call `await self._send_request("server/discover")`, get "result" from response and assign to `discover_result`
        #       - Get `supported_versions` from `discover_result.get("supportedVersions", [])`
        #       - If PROTOCOL_VERSION not in `supported_versions` raise
        #         RuntimeError(f"Server doesn't support {PROTOCOL_VERSION}, supported versions: {supported_versions}")
        #       - Print `discover_result` (capabilities and info of MCP Server): `print(json.dumps(discover_result, indent=2))`
        # 5. Catch Exception as `e`, call `await self.close()` and raise RuntimeError(f"Failed to connect to MCP server: {e}")
        raise NotImplementedError()

    async def close(self) -> None:
        """Close HTTP session"""
        if self.http_session:
            await self.http_session.close()
            self.http_session = None

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        #TODO:
        # 1. Check if `self.http_session` is None, raise RuntimeError("MCP client not connected. Call connect() first.") if so
        # 2. Call `await self._send_request("tools/list")` and assign to `response`
        # 3. Extract tools from response: `tools = response["result"]["tools"]`
        # 4. Iterate through `tools` and return list comprehension that transforms each tool in tools to:
        #       {
        #           "type": "function",
        #           "function": {
        #               "name": tool["name"],
        #               "description": tool.get("description", ""),
        #               "parameters": tool.get("inputSchema", {})
        #           }
        #       }
        raise NotImplementedError()

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        #TODO:
        # 1. Check if `self.http_session` is None, raise RuntimeError("MCP client not connected. Call connect() first.") if so
        # 2. print(f"    Calling `{tool_name}` with {tool_args}")
        # 3. Create `params` dictionary with:
        #       - "name": tool_name
        #       - "arguments": tool_args
        # 4. Call `await self._send_request("tools/call", params)` and assign to `response`
        #       response sample:
        #       {
        #           "jsonrpc": "2.0",
        #           "id": 1,
        #           "result": {
        #               "content": [
        #                   {
        #                       "type": "text",
        #                       "text": "some tool call result"
        #                   }
        #                ],
        #               "isError": false,
        #               "resultType": "complete"
        #           }
        #       }
        # 5. Extract content using walrus operator: `if content:= response["result"].get("content", [])`
        # 6. Extract first item using walrus operator: `if item := content[0]`
        # 7. Extract text result: `text_result = item.get("text", "")`
        # 8. print(f"    ⚙️: {text_result}\n")
        # 9. Return `text_result`
        # 10. If no content found, return "Unexpected error occurred!"
        raise NotImplementedError()
