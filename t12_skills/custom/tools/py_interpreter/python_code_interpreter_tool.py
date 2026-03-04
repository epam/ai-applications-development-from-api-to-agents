from pathlib import Path
from typing import Any, Optional

from t12_skills.custom.file_utils import get_file_content
from t12_skills.custom.mcp.mcp_client import T12MCPClient
from t12_skills.custom.mcp.mcp_tool_model import MCPToolModel
from t12_skills.custom.tools.base import BaseTool
from t12_skills.custom.tools.py_interpreter._response import _ExecutionResult


class PythonCodeInterpreterTool(BaseTool):

    def __init__(
            self,
            mcp_client: T12MCPClient,
            mcp_tool_models: list[MCPToolModel],
            tool_name: str,
            skills_dir: Path
    ):
        self._mcp_client = mcp_client
        self._skills_dir = skills_dir

        self._code_execute_tool: Optional[MCPToolModel] = None
        for mcp_tool_model in mcp_tool_models:
            if mcp_tool_model.name == tool_name:
                self._code_execute_tool = mcp_tool_model

        if not self._code_execute_tool:
            available = [m.name for m in mcp_tool_models]
            raise ValueError(
                f"MCP server doesn't have `{tool_name}` tool. Available: {available}"
            )

    @classmethod
    async def create(
            cls,
            mcp_url: str,
            tool_name: str,
            skills_dir: Path
    ) -> 'PythonCodeInterpreterTool':
        """Async factory method to create PythonCodeInterpreterTool."""
        mcp_client = await T12MCPClient.create(mcp_url)
        tools = await mcp_client.get_tools()
        return cls(
            mcp_client=mcp_client,
            mcp_tool_models=tools,
            tool_name=tool_name,
            skills_dir=skills_dir,
        )

    @property
    def name(self) -> str:
        return self._code_execute_tool.name

    @property
    def description(self) -> str:
        return self._code_execute_tool.description

    @property
    def parameters(self) -> dict[str, Any]:
        result = {
            **self._code_execute_tool.parameters,
        }
        result["properties"]["script_path"] = {
            "type": "string",
            "description": "Path with python script to upload to code interpreter. Will be combined with `code` in such way: code from file by `script_path` + \n\n + `code`."
        }
        return result

    async def _execute(self, arguments: dict[str, Any]) -> str:
        args: dict[str, Any] = {}

        if arguments.get("script_path", None):
            full_path = (self._skills_dir / arguments.get("script_path").lstrip("/")).resolve()
            script_content = get_file_content(full_path)
            args["code"] = f"{script_content}\n\n{arguments.get('code', '')}"
            args["session_id"] = arguments.get('session_id', '')
        else:
            args = arguments

        content = await self._mcp_client.call_tool(self.name, args)
        execution_result = _ExecutionResult.model_validate_json(content)
        return execution_result.model_dump_json()
