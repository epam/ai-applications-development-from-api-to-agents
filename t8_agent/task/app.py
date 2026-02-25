from commons.constants import OPENAI_API_KEY, ANTHROPIC_API_KEY
from commons.models.conversation import Conversation
from commons.models.message import Message
from commons.models.role import Role
from commons.user_service.client import UserServiceClient

from t8_agent.task.agents.anthropic import AnthropicBasedAgent
from t8_agent.task.agents.openai import OpenAIBasedAgent
from t8_agent.task.prompts import SYSTEM_PROMPT
from t8_agent.task.tools.users.create_user_tool import CreateUserTool
from t8_agent.task.tools.users.delete_user_tool import DeleteUserTool
from t8_agent.task.tools.users.get_user_by_id_tool import GetUserByIdTool
from t8_agent.task.tools.users.search_users_tool import SearchUsersTool
from t8_agent.task.tools.users.update_user_tool import UpdateUserTool
from t8_agent.task.tools.web_search import WebSearchTool


def main():
    #TODO:
    # 1. Create UserClient
    # 2. Create tools (WebSearchTool, GetUserByIdTool, SearchUsersTool, CreateUserTool, UpdateUserTool, DeleteUserTool)
    # 3. Create OpenAIClient with all tools and SYSTEM_PROMPT, as model can use gpt-5.2
    # 4.. Create Conversation

    print("Type your question or 'exit' to quit.")
    print("Sample:")
    print("Add Andrej Karpathy as a new user")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
        #TODO:
        # 1. Add User message to Conversation
        # 2. Call agent with conversation history
        # 3. Add Assistant message to Conversation and print its content

        print("=" * 100)
        print()


main()
