from typing import Optional

from mcp import Client
from mcp.client.stdio import StdioServerParameters

from t9_mcp_fundamentals.agent.mcp_clients.base import MCPClient


class StdioMCPClient(MCPClient):
    """
    Handles MCP server connection and tool execution via stdio.

    Supports two launch modes:
      1. Docker image  — pass docker_image="mcp/duckduckgo:latest"
      2. Local script  — pass command="python", args=["path/to/stdio_server.py"]

    In both cases the MCP protocol runs over the process's stdin/stdout.
    You do NOT need to start the process manually; the client spawns it for you.

    Usage examples:
        # Docker
        async with StdioMCPClient(docker_image="mcp/duckduckgo:latest") as client:
            ...

        # Local stdio server
        async with StdioMCPClient(command="python", args=["t9_mcp_fundamentals/mcp_server/stdio_server.py"]) as client:
            ...
    """

    def __init__(
            self,
            docker_image: Optional[str] = None,
            command: Optional[str] = None,
            args: Optional[list[str]] = None,
            env: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Args:
            docker_image: Docker image name. When provided, the client runs
                          `docker run --rm -i <docker_image>` to launch the server.
            command:      Executable to run for a local stdio server (e.g. "python").
                          Ignored when docker_image is set.
            args:         Arguments for the local executable
                          (e.g. ["path/to/stdio_server.py"]).
            env:          Optional environment variables forwarded to the process.
        """
        if docker_image is None and command is None:
            raise ValueError("Provide either 'docker_image' or 'command' to launch the MCP server.")

        super().__init__()
        self.docker_image = docker_image
        self.command = command
        self.args = args or []
        self.env = env

    def _build_server_params(self) -> StdioServerParameters:
        #TODO:
        # 1. If `self.docker_image` is set, return `StdioServerParameters` with:
        #    - command="docker"
        #    - args=["run", "--rm", "-i", self.docker_image]
        #    - env=self.env
        # 2. Otherwise return `StdioServerParameters` with:
        #    - command=self.command
        #    - args=self.args
        #    - env=self.env
        raise NotImplementedError()

    def _startup_message(self) -> str:
        if self.docker_image:
            return (
                f"Starting Docker container: {self.docker_image}\n"
                f"To inspect running containers: docker ps --filter 'ancestor={self.docker_image}'"
            )
        return f"Starting local stdio server: {self.command} {' '.join(self.args)}"

    async def __aenter__(self):
        #TODO:
        # 1. Call `_build_server_params()` and assign to `server_params`
        # 2. Print `_startup_message()`
        # 3. Create `Client(server_params)` and assign to `self.client` (Client spawns the process)
        # 4. Call `await self.client.__aenter__()`. Client sends `server/discover` first. Servers that don't support
        #    stateless MCP (2026-07-28) answer with an error and Client falls back to the legacy `initialize` handshake
        # 5. Print f"Connected to {self.client.server_info} (protocol version {self.client.protocol_version})" and
        #    f"Capabilities: {self.client.server_capabilities.model_dump_json(indent=2, exclude_none=True)}"
        # 6. Return self
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        #TODO:
        # This is the shutdown method.
        # If `self.client` is present, call `await self.client.__aexit__(exc_type, exc_val, exc_tb)` and set `self.client = None`
        raise NotImplementedError()
