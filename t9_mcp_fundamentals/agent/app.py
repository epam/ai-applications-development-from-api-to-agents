import os
import sys
import asyncio
import json
from pathlib import Path

from mcp import Resource
from mcp.types import Prompt

from commons.constants import OPENAI_API_KEY
from commons.models.message import Message
from commons.models.role import Role
from t9_mcp_fundamentals.agent.agent import AgentMCPFundamentals
from t9_mcp_fundamentals.agent.mcp_clients.http import HttpMCPClient
from t9_mcp_fundamentals.agent.mcp_clients.stdio import StdioMCPClient
from t9_mcp_fundamentals.agent.prompts import SYSTEM_PROMPT


PROJECT_ROOT = Path(__file__).parent.parent.parent  # .../ai-applications-development-from-api-to-agents
STDIO_SERVER_PATH = PROJECT_ROOT / "t9_mcp_fundamentals" / "mcp_server" / "stdio_server.py"

async def main():
    #TODO:
    # 1. Use `StdioMCPClient` as async context manager with command="python" and args=[str(STDIO_SERVER_PATH)],
    #    assign it to `mcp_client`
    # 2. Print "\n=== Available Resources ===" and fetch resources via `mcp_client.get_resources()`,
    #    iterate and print each resource
    # 3. Print "\n=== Available Tools ===" and fetch tools via `mcp_client.get_tools()`,
    #    iterate and print each tool with `json.dumps(tool, indent=2)`
    # 4. Create `AgentMCPFundamentals` with api_key=OPENAI_API_KEY, model="gpt-5.2", tools=tools,
    #    mcp_client=mcp_client and assign it to `agent`
    # 5. Create `messages` list with a single system Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)
    # 6. Print "\n=== Available Prompts ===" and fetch prompts via `mcp_client.get_prompts()`.
    #    For each prompt:
    #      - print the prompt
    #      - get its content with `mcp_client.get_prompt(prompt.name)` and print it
    #      - append Message(role=Role.USER, content=f"## Prompt provided by MCP server:\n{prompt.description}\n{content}")
    #        to `messages`
    # 7. Print "MCP-based Agent is ready! Type your query or 'exit' to exit."
    # 8. Run a chat loop:
    #      - read user input with `input("\n> ").strip()`
    #      - break if input is 'exit'
    #      - append Message(role=Role.USER, content=user_input) to messages
    #      - call `await agent.get_completion(messages)`, append the result to messages
    raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(main())
