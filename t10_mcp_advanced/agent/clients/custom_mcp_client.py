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
        if not self.http_session:
            raise RuntimeError("HTTP session not initialized")

        # There is no session: every request carries protocol version, client info and capabilities in `_meta`
        request_data: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": {
                **(params or {}),
                "_meta": {
                    "io.modelcontextprotocol/protocolVersion": PROTOCOL_VERSION,
                    "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
                    "io.modelcontextprotocol/clientCapabilities": {}
                }
            }
        }

        # Protocol version, method and tool name are mirrored into headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PROTOCOL_VERSION,
            "Mcp-Method": method
        }
        if method == "tools/call":
            headers["Mcp-Name"] = self._encode_header_value(params["name"])

        async with self.http_session.post(
                self.server_url,
                json=request_data,
                headers=headers
        ) as response:
            # Check content type to determine parsing strategy
            content_type = response.headers.get('content-type', '').lower()

            if 'text/event-stream' in content_type:
                response_data = await self._parse_sse_response_streaming(response)
            elif 'application/json' in content_type:
                # Regular JSON response. Errors (4xx) are also returned as JSON
                response_data = await response.json()
            else:
                raise RuntimeError(f"Unexpected response (HTTP {response.status}): {await response.text()}")

            if "error" in response_data:
                error = response_data["error"]
                raise RuntimeError(f"MCP Error {error['code']}: {error['message']}")

            # `input_required` results (Multi Round-Trip Requests) are not supported by this client
            result_type = response_data["result"].get("resultType", "complete")
            if result_type != "complete":
                raise RuntimeError(f"Unsupported resultType: {result_type}")

            return response_data

    async def _parse_sse_response_streaming(self, response: aiohttp.ClientResponse) -> dict[str, Any]:
        """Parse Server-Sent Events response with streaming"""
        async for line in response.content:
            line_str = line.decode('utf-8').strip()

            # Skip empty lines, comments (`:`) and other SSE fields like `event: message`
            if not line_str.startswith('data:'):
                continue

            data_part = line_str[5:].strip()
            if not data_part:
                continue

            try:
                message = json.loads(data_part)
            except json.JSONDecodeError:
                continue

            # The server may send notifications (e.g. progress) before the final response. Only response has `id`
            if "id" in message:
                return message

        raise RuntimeError("No JSON-RPC response found in SSE stream")

    async def connect(self) -> None:
        """Create HTTP session and discover MCP server (no handshake and no session in stateless MCP)"""
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
        self.http_session = aiohttp.ClientSession(timeout=timeout, connector=connector)

        try:
            discover_result = (await self._send_request("server/discover"))["result"]
            supported_versions = discover_result.get("supportedVersions", [])
            if PROTOCOL_VERSION not in supported_versions:
                raise RuntimeError(f"Server doesn't support {PROTOCOL_VERSION}, supported versions: {supported_versions}")
            print(json.dumps(discover_result, indent=2))
        except Exception as e:
            await self.close()
            raise RuntimeError(f"Failed to connect to MCP server: {e}")

    async def close(self) -> None:
        """Close HTTP session"""
        if self.http_session:
            await self.http_session.close()
            self.http_session = None

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        if not self.http_session:
            raise RuntimeError("MCP client not connected. Call connect() first.")

        response = await self._send_request("tools/list")
        tools = response["result"]["tools"]
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {})
                }
            }
            for tool in tools
        ]

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        if not self.http_session:
            raise RuntimeError("MCP client not connected. Call connect() first.")

        print(f"    Calling `{tool_name}` with {tool_args}")

        params = {
            "name": tool_name,
            "arguments": tool_args
        }

        response = await self._send_request("tools/call", params)

        if content := response["result"].get("content", []):
            if item := content[0]:
                text_result = item.get("text", "")
                print(f"    ⚙️: {text_result}\n")
                return text_result

        return "Unexpected error occurred!"
