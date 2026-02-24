from commons.constants import OPENAI_API_KEY, ANTHROPIC_API_KEY
from commons.user_service.client import UserServiceClient
from t8_agent.task._models.conversation import Conversation
from t8_agent.task._models.message import Message
from t8_agent.task._models.role import Role
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
    # 2. Create list with all tools (WebSearchTool, GetUserByIdTool, SearchUsersTool, CreateUserTool, UpdateUserTool, DeleteUserTool)
    # 3. Create OpenAIBasedAgent with all tools (or AnthropicBasedAgent)
    # 4. Create Conversation
    # 5. Run infinite loop and in loop and:
    #    - get user input from terminal (`input("> ").strip()`)
    #    - Add User message to Conversation
    #    - Call OpenAIClient with conversation history
    #    - Add Assistant message to Conversation and print its content
    raise NotImplementedError()


main()
