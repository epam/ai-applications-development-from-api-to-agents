from t2_llms_output_tuning._clients._base_client import AIClient
from t2_llms_output_tuning._models.conversation import Conversation
from t2_llms_output_tuning._models.message import Message
from t2_llms_output_tuning._models.role import Role


def run(
        client: AIClient,
        print_request: bool = True,
        print_only_content: bool = False,
        **kwargs
) -> None:
    conversation = Conversation()

    print("Type your question or 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
    
        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
    
        conversation.add_message(Message(Role.USER, user_input))

        print("AI:")
        ai_message = client.response(
            messages=conversation.get_messages(),
            print_request=print_request,
            print_only_content=print_only_content,
            **kwargs
        )
        conversation.add_message(ai_message)
