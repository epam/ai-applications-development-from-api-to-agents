import asyncio
import json

from commons.constants import OPENAI_API_KEY, DEFAULT_SYSTEM_PROMPT
from commons.models.message import Message
from commons.models.role import Role
from t11_mcp_auth.agent._agent import AgentMCPAuth
from t11_mcp_auth.agent.mcp_clients.api_key_mcp_client import ApiKeyMCPClient
from t11_mcp_auth.agent.mcp_clients.oauth_mcp_client import OauthHttpMCPClient

MCP_API_KEY: str = "dev-secret-key"

async def main():
    #TODO:
    # 1. Use one of the clients as async context manager, assign to `mcp_client`:
    #       - `ApiKeyMCPClient(mcp_server_url="http://localhost:8007/mcp", api_key=MCP_API_KEY)`
    #       - OR `OauthHttpMCPClient(mcp_server_url="http://localhost:8008/mcp")`
    # 2. Print "\n=== Available Tools ===" and fetch tools via `mcp_client.get_tools()`,
    #    assign to `tools`; iterate and print each with `json.dumps(tool, indent=2)`
    # 3. Create `AgentMCPAuth` instance with:
    #       - api_key=OPENAI_API_KEY
    #       - model="gpt-5.2"
    #       - tools=tools
    #       - mcp_client=mcp_client
    #    assign to `agent`
    # 4. Create initial `messages` list with a single
    #    `Message(role=Role.SYSTEM, content=DEFAULT_SYSTEM_PROMPT)`
    # 5. Print "MCP-based Agent is ready! Type your query or 'exit' to exit."
    #    Run a loop: read user input with `input("\n> ").strip()`, break on "exit",
    #    append `Message(role=Role.USER, content=user_input)` to `messages`,
    #    await `agent.get_completion(messages)`, assign to `ai_message`,
    #    append `ai_message` to `messages`
    raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(main())