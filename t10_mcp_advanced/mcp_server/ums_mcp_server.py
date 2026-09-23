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
        #TODO:
        # 1. Create UserServiceClient
        # 2. Create list of tools: GetUserByIdTool, SearchUsersTool, CreateUserTool, UpdateUserTool, DeleteUserTool
        # 3. Iterate trough list and add them to `self.tools` dict where key is tool name and value is tool itself
        raise NotImplementedError()

    def _complete_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """Every final result has `resultType: "complete"` and identifies the server in its `_meta`"""
        return {
            **result,
            "resultType": "complete",
            "_meta": {SERVER_INFO_META_KEY: self.server_info}
        }

    def validate_request_meta(self, request: MCPRequest) -> MCPResponse | None:
        """Validate per-request protocol fields. Returns an error response if the request can't be processed"""
        #TODO:
        # 1. Get `meta` from request params: `(request.params or {}).get("_meta") or {}`
        # 2. Collect `missing_keys`: keys from (PROTOCOL_VERSION_META_KEY, CLIENT_CAPABILITIES_META_KEY) that are not in `meta`
        # 3. If `missing_keys` present, return MCPResponse with error:
        #       - id=request.id
        #       - error=ErrorResponse(code=-32602, message=f"params._meta is missing required key(s): {', '.join(missing_keys)}")
        # 4. Get `protocol_version` from `meta[PROTOCOL_VERSION_META_KEY]`
        # 5. If `protocol_version` not in `self.supported_versions`, return MCPResponse with error:
        #       - id=request.id
        #       - error=ErrorResponse(
        #             code=UNSUPPORTED_PROTOCOL_VERSION_ERROR_CODE,
        #             message="Unsupported protocol version",
        #             data={"supported": self.supported_versions, "requested": protocol_version}
        #         )
        # 6. Return None
        raise NotImplementedError()

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
        #TODO:
        # 1. Create MCPResponse:
        #       - id=request.id
        #       - result=self._complete_result(
        #             {
        #                 "supportedVersions": self.supported_versions,
        #                 "capabilities": {
        #                     "tools": {"listChanged": False}
        #                 },
        #                 "instructions": "Users Management Service tools: search, get, create, update and delete users.",
        #                 "ttlMs": 3600000,
        #                 "cacheScope": "public"
        #             }
        #         )
        #    `ttlMs` and `cacheScope` are caching hints, they are required for server/discover and list results
        # 2. Return created MCP response
        raise NotImplementedError()

    def handle_tools_list(self, request: MCPRequest) -> MCPResponse:
        """Handle tools/list request"""
        #TODO:
        # 1. Create `tools_list` by iterating through `self.tools.values()` and calling `to_mcp_tool()` on each tool (via comprehension)
        # 2. Create MCPResponse:
        #       - id=request.id
        #       - result=self._complete_result({"tools": tools_list, "ttlMs": 300000, "cacheScope": "public"})
        # 3. Return created MCP response
        raise NotImplementedError()

    async def handle_tools_call(self, request: MCPRequest) -> MCPResponse:
        """Handle tools/call request with proper MCP-compliant response format"""
        #TODO:
        # 1. Extract `tool_name` from `request.params.get("name")` and `arguments` from `request.params.get("arguments", {})`
        # 2. Check if `tool_name` exists, if not return MCPResponse with error:
        #       - id=request.id
        #       - error=ErrorResponse(code=-32602, message="Missing required parameter: name")
        # 3. Check if `tool_name` exists in `self.tools`, if not return MCPResponse with error:
        #       - id=request.id
        #       - error=ErrorResponse(code=-32602, message=f"Unknown tool: {tool_name}")
        # 4. Get `tool` from `self.tools[tool_name]`
        # 5. Try to execute tool with arguments:
        #       - Call `await tool.execute(arguments)` and assign result to `result_text`
        #       - Return MCPResponse with:
        #           - id=request.id
        #           - result=self._complete_result({"content": [{"type": "text", "text": result_text}], "isError": False})
        # 6. Handle exceptions by returning MCPResponse with:
        #       - id=request.id
        #       - result=self._complete_result({"content": [{"type": "text", "text": f"Tool execution error: {str(tool_error)}"}], "isError": True})
        raise NotImplementedError()
