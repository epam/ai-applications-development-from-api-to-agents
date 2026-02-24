import asyncio
from typing import Any

from openai import AsyncOpenAI

from commons.constants import OPENAI_API_KEY
from t6_grounding.user_service_client import UserServiceClient

BATCH_SYSTEM_PROMPT = """You are a user search assistant. Your task is to find users from the provided list that match the search criteria.

INSTRUCTIONS:
1. Analyze the user question to understand what attributes/characteristics are being searched for
2. Examine each user in the context and determine if they match the search criteria
3. For matching users, extract and return their complete information
4. Be inclusive - if a user partially matches or could potentially match, include them

OUTPUT FORMAT:
- If you find matching users: Return their full details exactly as provided, maintaining the original format
- If no users match: Respond with exactly "NO_MATCHES_FOUND"
- If uncertain about a match: Include the user with a note about why they might match"""

FINAL_SYSTEM_PROMPT = """You are a helpful assistant that provides comprehensive answers based on user search results.

INSTRUCTIONS:
1. Review all the search results from different user batches
2. Combine and deduplicate any matching users found across batches
3. Present the information in a clear, organized manner
4. If multiple users match, group them logically
5. If no users match, explain what was searched for and suggest alternatives"""

USER_PROMPT = """## USER DATA:
{context}

## SEARCH QUERY: 
{query}"""


class TokenTracker:
    def __init__(self):
        self.total_tokens = 0
        self.batch_tokens = []

    def add_tokens(self, tokens: int):
        self.total_tokens += tokens
        self.batch_tokens.append(tokens)

    def get_summary(self):
        return {
            'total_tokens': self.total_tokens,
            'batch_count': len(self.batch_tokens),
            'batch_tokens': self.batch_tokens
        }


llm_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

token_tracker = TokenTracker()


def join_context(context: list[dict[str, Any]]) -> str:
    context_str = ""
    for user in context:
        context_str += f"User:\n"
        for key, value in user.items():
            context_str += f"  {key}: {value}\n"
        context_str += "\n"
    return context_str


async def generate_response(system_prompt: str, user_message: str) -> str:
    print("Processing...")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    response = await llm_client.chat.completions.create(
        model='gpt-4.1-nano',
        temperature=0.0,
        messages=messages,
    )
    total_tokens = response.usage.total_tokens if response.usage else 0

    token_tracker.add_tokens(total_tokens)

    content = response.choices[0].message.content or ""
    print(f"Response: \n {content}\nTokens used: {total_tokens}\n")
    return content


async def main():
    print("Query samples:")
    print(" - Do we have someone with name John that loves traveling?")

    user_question = input("> ").strip()
    if user_question:
        print("\n--- Searching user database ---")

        users = UserServiceClient().get_all_users()
        user_batches = [users[i:i + 100] for i in range(0, len(users), 100)]

        # Process batches to find relevant users
        tasks = [
            generate_response(
                system_prompt=BATCH_SYSTEM_PROMPT,
                user_message=USER_PROMPT.format(
                    context=join_context(user_batch),
                    query=user_question
                )
            )
            for user_batch in user_batches
        ]
        batch_results = await asyncio.gather(*tasks)

        print("\n--- Compiling results ---")

        relevant_results = [result for result in batch_results if result.strip() != "NO_MATCHES_FOUND"]

        print(f"\n=== SEARCH RESULTS ===")
        if relevant_results:
            combined_results = "\n\n".join(relevant_results)

            await generate_response(
                system_prompt=FINAL_SYSTEM_PROMPT,
                user_message=f"SEARCH RESULTS:\n{combined_results}\n\nORIGINAL QUERY: {user_question}"
            )

        else:
            print(f"\n=== SEARCH RESULTS ===")
            print(f"No users found matching '{user_question}'")
            print("\nTry refining your search or using different keywords.")

        summary = token_tracker.get_summary()
        print(f"\n=== Performance ===")
        print(f"Total API calls: {summary['batch_count']}")
        print(f"Total tokens: {summary['total_tokens']}")


if __name__ == "__main__":
    asyncio.run(main())


# The problems with No Grounding approach are:
#   - If we load whole users as context in one request to LLM we will hit context window
#   - Huge token usage == Higher price per request
#   - Added + one chain in flow where original user data can be changed by LLM (before final generation)
# User Question -> Get all users -> ‼️parallel search of possible candidates‼️ -> probably changed original context -> final generation