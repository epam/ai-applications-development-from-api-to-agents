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
    user_client = UserServiceClient()
    tools=[
        WebSearchTool(open_ai_api_key=OPENAI_API_KEY),
        GetUserByIdTool(user_client),
        SearchUsersTool(user_client),
        CreateUserTool(user_client),
        UpdateUserTool(user_client),
        DeleteUserTool(user_client),
    ]

    # agent = OpenAIBasedAgent(
    #     model="gpt-5.2",
    #     api_key=OPENAI_API_KEY,
    #     tools=tools,
    #     system_prompt=SYSTEM_PROMPT,
    # )
    agent = AnthropicBasedAgent(
        model="claude-sonnet-4-5",
        api_key=ANTHROPIC_API_KEY,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )

    conversation = Conversation()

    print("Type your question or 'exit' to quit.")
    print("Sample:")
    print("Add Andrej Karpathy as a new user")

    while True:
        user_input = input("> ").strip()

        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        conversation.add_message(Message(Role.USER, user_input))

        ai_message = agent.get_response(conversation.get_messages(), print_request=True)
        conversation.add_message(ai_message)
        print("🤖:", ai_message.content)
        print("=" * 100)
        print()


main()
