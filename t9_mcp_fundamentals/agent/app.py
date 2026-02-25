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


# https://remote.mcpservers.org/fetch/mcp
# Pay attention that `fetch` doesn't have resources and prompts

PROJECT_ROOT = Path(__file__).parent.parent.parent  # .../ai-applications-development-from-api-to-agents
STDIO_SERVER_PATH = PROJECT_ROOT / "t9_mcp_fundamentals" / "mcp_server" / "stdio_server.py"

async def main():
    async with StdioMCPClient(
            command=sys.executable,          # use the same venv Python, not bare "python"
            args=[str(STDIO_SERVER_PATH)],
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}  # inherit env + add project root
    ) as mcp_client:
    # async with StdioMCPClient(docker_image="mcp/duckduckgo:latest") as mcp_client:
    # async with HttpMCPClient(mcp_server_url="http://localhost:8005/mcp") as mcp_client:
        print("\n=== Available Resources ===")
        resources: list[Resource] = await mcp_client.get_resources()
        for resource in resources:
            print(resource)

        print("\n=== Available Tools ===")
        tools: list[dict] = await mcp_client.get_tools()
        for tool in tools:
            print(json.dumps(tool, indent=2))

        dial_client = AgentMCPFundamentals(
            api_key=OPENAI_API_KEY,
            model="gpt-5.2",
            tools=tools,
            mcp_client=mcp_client
        )

        messages: list[Message] = [
            Message(
                role=Role.SYSTEM,
                content=SYSTEM_PROMPT
            )
        ]

        print("\n=== Available Prompts ===")
        prompts: list[Prompt] = await mcp_client.get_prompts()
        for prompt in prompts:
            print(prompt)
            content = await mcp_client.get_prompt(prompt.name)
            print(content)
            messages.append(
                Message(
                    role=Role.USER,
                    content=f"## Prompt provided by MCP server:\n{prompt.description}\n{content}"
                )
            )

        print("MCP-based Agent is ready! Type your query or 'exit' to exit.")
        while True:
            user_input = input("\n> ").strip()
            if user_input.lower() == 'exit':
                break

            messages.append(
                Message(
                    role=Role.USER,
                    content=user_input
                )
            )

            ai_message: Message = await dial_client.get_completion(messages)
            messages.append(ai_message)


if __name__ == "__main__":
    asyncio.run(main())
