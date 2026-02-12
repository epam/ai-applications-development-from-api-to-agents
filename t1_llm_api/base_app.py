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
    #TODO:
    # Main chat loop that handles user interaction with AI clients.
    # 1. Create a new Conversation object to maintain chat history
    # 2. Print to console: `Type your question or 'exit' to quit.`
    # 3. Create infinite `while` loop
    # 4. Get user input from console, use `input` method
    # 5. If user_input is `exit` then `break` the loop
    # 6. Add user message to conversation (role is "user", content is user_input)
    # 7.1. If `stream` is true than call `client.stream_completion` with messages (it's async, don't forget to await)
    # 7.2. Otherwise call `client.get_completion` with messages
    # 7.3. Get Assistant message and add it to the conversation
    raise NotImplementedError
