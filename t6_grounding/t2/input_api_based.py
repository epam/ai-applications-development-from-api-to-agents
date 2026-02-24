from enum import StrEnum
from typing import Any

from openai import OpenAI
from pydantic import BaseModel, Field

from commons.constants import OPENAI_API_KEY
from t6_grounding.user_service_client import UserServiceClient

QUERY_ANALYSIS_PROMPT = """You are a query analysis system that extracts search parameters from user questions about users.

## Available Search Fields:
- **name**: User's first name (e.g., "John", "Mary")
- **surname**: User's last name (e.g., "Smith", "Johnson") 
- **email**: User's email address (e.g., "john@example.com")

## Instructions:
1. Analyze the user's question and identify what they're looking for
2. Extract specific search values mentioned in the query
3. Map them to the appropriate search fields
4. If multiple search criteria are mentioned, include all of them
5. Only extract explicit values - don't infer or assume values not mentioned

## Examples:
- "Who is John?" → name: "John"
- "Find users with surname Smith" → surname: "Smith" 
- "Look for john@example.com" → email: "john@example.com"
- "Find John Smith" → name: "John", surname: "Smith"
- "I need user emails that filled with hiking" → No clear search parameters (return empty list)
"""

SYSTEM_PROMPT = """You are a RAG-powered assistant that assists users with their questions about user information.
            
## Structure of User message:
`RAG CONTEXT` - Retrieved documents relevant to the query.
`USER QUESTION` - The user's actual question.

## Instructions:
- Use information from `RAG CONTEXT` as context when answering the `USER QUESTION`.
- Cite specific sources when using information from the context.
- Answer ONLY based on conversation history and RAG context.
- If no relevant information exists in `RAG CONTEXT` or conversation history, state that you cannot answer the question.
- Be conversational and helpful in your responses.
- When presenting user information, format it clearly and include relevant details.
"""

USER_PROMPT = """## RAG CONTEXT:
{context}

## USER QUESTION: 
{query}"""


class SearchField(StrEnum):
    NAME = "name"
    SURNAME = "surname"
    EMAIL = "email"


class SearchRequest(BaseModel):
    search_field: SearchField = Field(description="Search field")
    search_value: str = Field(description="Search value. Sample: Adam.")


class SearchRequests(BaseModel):
    search_request_parameters: list[SearchRequest] = Field(
        description="List of search parameters to execute",
        default_factory=list
    )


llm_client = OpenAI(api_key=OPENAI_API_KEY)

user_client = UserServiceClient()


def retrieve_context(user_question: str) -> list[dict[str, Any]]:
    """Extract search parameters from user query and retrieve matching users."""
    messages = [
        {"role": "system", "content": QUERY_ANALYSIS_PROMPT},
        {"role": "user", "content": user_question},
    ]

    response = llm_client.beta.chat.completions.parse(
        model='gpt-4.1-nano',
        temperature=0.0,
        messages=messages,
        response_format=SearchRequests,
    )
    search_requests: SearchRequests = response.choices[0].message.parsed

    if search_requests.search_request_parameters:
        requests_dict = {}
        for search_request in search_requests.search_request_parameters:
            requests_dict[search_request.search_field.value] = search_request.search_value

        print(f"Searching with parameters: {requests_dict}")
        return user_client.search_users(**requests_dict)

    print("No specific search parameters found!")
    return []


def augment_prompt(user_question: str, context: list[dict[str, Any]]) -> str:
    """Combine user query with retrieved context into a formatted prompt."""
    context_str = ""
    for user in context:
        context_str += f"User:\n"
        for key, value in user.items():
            context_str += f"  {key}: {value}\n"
        context_str += "\n"

    augmented_prompt = USER_PROMPT.format(context=context_str, query=user_question)
    print(augmented_prompt)
    return augmented_prompt


def generate_answer(augmented_prompt: str) -> str:
    """Generate final answer using the augmented prompt."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": augmented_prompt},
    ]

    response = llm_client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.0,
        messages=messages,
    )
    return response.choices[0].message.content or ""


def main():
    print("Query samples:")
    print(" - I need user emails that filled with hiking and psychology")
    print(" - Who is John?")
    print(" - Find users with surname Adams")
    print(" - Do we have smbd with name John that love painting?")

    while True:
        user_question = input("> ").strip()
        if user_question:
            if user_question.lower() in ['quit', 'exit']:
                break

            print("\n--- Retrieving context ---")
            context = retrieve_context(user_question)
            if context:
                print("\n--- Augmenting prompt ---")
                augmented_prompt = augment_prompt(user_question, context)

                print("\n--- Generating answer ---")
                answer = generate_answer(augmented_prompt)
                print(f"\nAnswer: {answer}\n")
            else:
                print("\n--- No relevant information found ---")


if __name__ == "__main__":
    main()


# The problems with API based Grounding approach are:
#   - We need a Pre-Step to figure out what field should be used for search (Takes time)
#   - Values for search should be correct (✅ John -> ❌ Jonh)
#   - Is not so flexible
# Benefits are:
#   - We fetch actual data (new users added and deleted every 5 minutes)
#   - Costs reduce