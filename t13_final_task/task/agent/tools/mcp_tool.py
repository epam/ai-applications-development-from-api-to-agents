from typing import Any

from t13_final_task.task.agent.clients.base_mcp_client import BaseMcpClient
from t13_final_task.task.agent.models import McpToolModel
from t13_final_task.task.agent.tools.base import BaseTool


class McpTool(BaseTool):
    """Reads files from the local skills directory by path."""

    def __init__(self, client: BaseMcpClient, mcp_tool_model: McpToolModel):
        self._client = client
        self._mcp_tool_model = mcp_tool_model

    async def _execute(self, arguments: dict[str, Any]) -> str:
        #TODO: delegate to self._client.call_tool(self.name, arguments)
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return self._mcp_tool_model.name

    @property
    def description(self) -> str:
        return self._mcp_tool_model.description

    @property
    def parameters(self) -> dict[str, Any]:
        return self._mcp_tool_model.parameters
