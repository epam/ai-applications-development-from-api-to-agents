from enum import StrEnum
from typing import Any

from openai import OpenAI
from pydantic import BaseModel, Field

from commons.constants import OPENAI_API_KEY
from t6_grounding.user_service_client import UserServiceClient

#TODO:
# Define QUERY_ANALYSIS_PROMPT - instructs the LLM to act as a query analysis system:
#   - Available search fields: name, surname, email
#   - Analyze the user question and extract explicit search values
#   - Map extracted values to the appropriate search fields
#   - Only extract values that are clearly stated - do not infer or assume
#   - Include examples: "Who is John?" → name: "John", "Find John Smith" → name: "John", surname: "Smith"
QUERY_ANALYSIS_PROMPT = None

#TODO:
# Define SYSTEM_PROMPT - instructs the LLM to act as a RAG-powered assistant:
#   - The user message contains two sections: RAG CONTEXT and USER QUESTION
#   - Answer ONLY based on the provided RAG CONTEXT and conversation history
#   - If no relevant information exists in RAG CONTEXT, state that the question cannot be answered
#   - Format user information clearly when presenting it
SYSTEM_PROMPT = None

#TODO:
# Define USER_PROMPT template with two placeholders:
#   - {context} - the retrieved user data formatted as text
#   - {query}   - the user's original question
USER_PROMPT = None


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
    #TODO:
    # - Build a messages list with QUERY_ANALYSIS_PROMPT as system and user_question as user
    # - Call llm_client.beta.chat.completions.parse with:
    #   - model='gpt-4.1-nano', temperature=0.0
    #   - response_format=SearchRequests
    # - Extract search_request_parameters from the parsed response
    # - If parameters exist:
    #   - Build a dict mapping search_field.value → search_value for each parameter
    #   - Print "Searching with parameters: {dict}"
    #   - Return user_client.search_users(**dict)
    # - If no parameters found, print "No specific search parameters found!" and return []
    raise NotImplementedError


def augment_prompt(user_question: str, context: list[dict[str, Any]]) -> str:
    #TODO:
    # - Format each user in context as a "User:\n  key: value\n" block (with blank line after each)
    # - Insert the formatted string into USER_PROMPT using .format(context=..., query=user_question)
    # - Print the augmented prompt
    # - Return the augmented prompt string
    raise NotImplementedError


def generate_answer(augmented_prompt: str) -> str:
    #TODO:
    # - Build a messages list with SYSTEM_PROMPT as system and augmented_prompt as user
    # - Call llm_client.chat.completions.create with model='gpt-4o-mini', temperature=0.0
    # - Return the response content string (default to "" if None)
    raise NotImplementedError


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

            #TODO:
            # - Print "\n--- Retrieving context ---"
            # - Call retrieve_context(user_question) and store in context
            # - If context is not empty:
            #   - Print "\n--- Augmenting prompt ---"
            #   - Call augment_prompt(user_question, context) and store in augmented_prompt
            #   - Print "\n--- Generating answer ---"
            #   - Call generate_answer(augmented_prompt), print "\nAnswer: {answer}\n"
            # - Otherwise: print "\n--- No relevant information found ---"
            raise NotImplementedError


if __name__ == "__main__":
    main()


# The problems with API based Grounding approach are:
#   - We need a Pre-Step to figure out what field should be used for search (Takes time)
#   - Values for search should be correct (✅ John -> ❌ Jonh)
#   - Is not so flexible
# Benefits are:
#   - We fetch actual data (new users added and deleted every 5 minutes)
#   - Costs reduce