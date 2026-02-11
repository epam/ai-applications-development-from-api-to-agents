from t1_llm_api._models.conversation import Conversation
from t1_llm_api._models.message import Message
from t1_llm_api._models.role import Role
from t1_llm_api.base_client import AIClient


async def start(stream: bool, client: AIClient) -> None:
    """
    Start an interactive chat session with an AI client.

    This function runs a continuous loop that:
    1. Prompts the user for input
    2. Sends the conversation history to the AI
    3. Displays the AI's response
    4. Maintains conversation context

    The loop continues until the user types 'exit'.

    Args:
        stream (bool): If True, use streaming responses (real-time token display).
                      If False, use synchronous responses (complete response at once).
        client (AIClient): The AI client instance to use for generating responses.
    """
    conversation = Conversation()

    print("Type your question or 'exit' to quit.")
    while True:
        user_input = input("➡️ ").strip()

        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        conversation.add_message(Message(Role.USER, user_input))

        print("🤖: ", end="")
        if stream:
            ai_message = await client.stream_response(conversation.get_messages())
        else:
            ai_message = client.response(conversation.get_messages())

        conversation.add_message(ai_message)
