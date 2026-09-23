from typing import Any

from commons.user_service.client import UserServiceClient
from t10_mcp_advanced.mcp_server.models.request import MCPRequest
from t10_mcp_advanced.mcp_server.models.response import MCPResponse, ErrorResponse
from t10_mcp_advanced.mcp_server.tools.users.create_user_tool import CreateUserTool
from t10_mcp_advanced.mcp_server.tools.users.delete_user_tool import DeleteUserTool
from t10_mcp_advanced.mcp_server.tools.users.get_user_by_id_tool import GetUserByIdTool
from t10_mcp_advanced.mcp_server.tools.users.search_users_tool import SearchUsersTool
from t10_mcp_advanced.mcp_server.tools.users.update_user_tool import UpdateUserTool

# Reserved `_meta` keys (https://modelcontextprotocol.io/specification/2026-07-28/basic/index#_meta)
PROTOCOL_VERSION_META_KEY = "io.modelcontextprotocol/protocolVersion"
CLIENT_CAPABILITIES_META_KEY = "io.modelcontextprotocol/clientCapabilities"
SERVER_INFO_META_KEY = "io.modelcontextprotocol/serverInfo"

# Error codes reserved by the MCP specification
UNSUPPORTED_PROTOCOL_VERSION_ERROR_CODE = -32022


class UmsMCPServer:
    """
    Stateless MCP server (protocol version 2026-07-28).

    There is no `initialize` handshake and no session: every request carries the protocol version and
    client capabilities in `params._meta`, so each request is validated and processed independently.
    """

    def __init__(self):
        self.supported_versions = ["2026-07-28"]
        self.server_info = {
            "name": "custom-ums-mcp-server",
            "version": "1.0.0"
        }

        self.tools = {}
        self._register_tools()

    def _register_tools(self):
        """Register all available tools"""
        user_client = UserServiceClient()
        for tool in [
            GetUserByIdTool(user_client),
            SearchUsersTool(user_client),
            CreateUserTool(user_client),
            UpdateUserTool(user_client),
            DeleteUserTool(user_client),
        ]:
            self.tools[tool.name] = tool

    def _complete_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """Every final result has `resultType: "complete"` and identifies the server in its `_meta`"""
        return {
            **result,
            "resultType": "complete",
            "_meta": {SERVER_INFO_META_KEY: self.server_info}
        }

    def validate_request_meta(self, request: MCPRequest) -> MCPResponse | None:
        """Validate per-request protocol fields. Returns an error response if the request can't be processed"""
        meta = (request.params or {}).get("_meta") or {}

        missing_keys = [key for key in (PROTOCOL_VERSION_META_KEY, CLIENT_CAPABILITIES_META_KEY) if key not in meta]
        if missing_keys:
            return MCPResponse(
                id=request.id,
                error=ErrorResponse(
                    code=-32602,
                    message=f"params._meta is missing required key(s): {', '.join(missing_keys)}"
                )
            )

        protocol_version = meta[PROTOCOL_VERSION_META_KEY]
        if protocol_version not in self.supported_versions:
            return MCPResponse(
                id=request.id,
                error=ErrorResponse(
                    code=UNSUPPORTED_PROTOCOL_VERSION_ERROR_CODE,
                    message="Unsupported protocol version",
                    data={"supported": self.supported_versions, "requested": protocol_version}
                )
            )

        return None

    def handle_legacy_initialize(self, request: MCPRequest) -> MCPResponse:
        """Legacy clients (2025-11-25 and earlier) start with `initialize`. Tell them which versions we support"""
        requested_version = (request.params or {}).get("protocolVersion")
        return MCPResponse(
            id=request.id,
            error=ErrorResponse(
                code=UNSUPPORTED_PROTOCOL_VERSION_ERROR_CODE,
                message=f"The initialize handshake is not supported. "
                        f"This server is stateless and supports protocol versions: {self.supported_versions}",
                data={"supported": self.supported_versions, "requested": requested_version}
            )
        )

    def handle_discover(self, request: MCPRequest) -> MCPResponse:
        """Handle server/discover request: supported versions, capabilities and server identity"""
        return MCPResponse(
            id=request.id,
            result=self._complete_result(
                {
                    "supportedVersions": self.supported_versions,
                    "capabilities": {
                        "tools": {"listChanged": False}
                    },
                    "instructions": "Users Management Service tools: search, get, create, update and delete users.",
                    # Caching hints are required for server/discover and list results
                    "ttlMs": 3600000,
                    "cacheScope": "public"
                }
            )
        )

    def handle_tools_list(self, request: MCPRequest) -> MCPResponse:
        """Handle tools/list request"""
        # Tools are registered once, so the order is deterministic (helps client caching and LLM prompt caching)
        tools_list = [tool.to_mcp_tool() for tool in self.tools.values()]
        return MCPResponse(
            id=request.id,
            result=self._complete_result(
                {
                    "tools": tools_list,
                    "ttlMs": 300000,
                    "cacheScope": "public"
                }
            )
        )

    async def handle_tools_call(self, request: MCPRequest) -> MCPResponse:
        """Handle tools/call request with proper MCP-compliant response format"""
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        print(request)

        if not tool_name:
            return MCPResponse(
                id=request.id,
                error=ErrorResponse(
                    code=-32602,
                    message="Missing required parameter: name"
                )
            )

        if tool_name not in self.tools:
            return MCPResponse(
                id=request.id,
                error=ErrorResponse(
                    code=-32602,
                    message=f"Unknown tool: {tool_name}"
                )
            )

        tool = self.tools[tool_name]

        try:
            result_text = await tool.execute(arguments)
            return MCPResponse(
                id=request.id,
                result=self._complete_result(
                    {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text
                            }
                        ],
                        "isError": False
                    }
                )
            )
        except Exception as tool_error:
            return MCPResponse(
                id=request.id,
                result=self._complete_result(
                    {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Tool execution error: {str(tool_error)}"
                            }
                        ],
                        "isError": True
                    }
                )
            )
