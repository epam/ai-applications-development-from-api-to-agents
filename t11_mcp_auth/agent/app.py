import asyncio
import json

from commons.constants import OPENAI_API_KEY, DEFAULT_SYSTEM_PROMPT
from commons.models.message import Message
from commons.models.role import Role
from t11_mcp_auth.agent._agent import AgentMCPAuth
from t11_mcp_auth.agent.mcp_clients.api_key_mcp_client import ApiKeyMCPClient
from t11_mcp_auth.agent.mcp_clients.oauth_mcp_client import OauthHttpMCPClient

MCP_API_KEY: str =  "dev-secret-key"

async def main():

    # async with HttpMCPClient(mcp_server_url="http://localhost:8007/mcp",  api_key=MCP_API_KEY) as mcp_client:
    async with OauthHttpMCPClient(mcp_server_url="http://localhost:8008/mcp") as mcp_client:

        print("\n=== Available Tools ===")
        tools: list[dict] = await mcp_client.get_tools()
        for tool in tools:
            print(json.dumps(tool, indent=2))

        dial_client = AgentMCPAuth(
            api_key=OPENAI_API_KEY,
            model="gpt-5.2",
            tools=tools,
            mcp_client=mcp_client
        )

        messages: list[Message] = [
            Message(
                role=Role.SYSTEM,
                content=DEFAULT_SYSTEM_PROMPT
            )
        ]

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
