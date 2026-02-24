import asyncio
from typing import Any

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from commons.constants import OPENAI_API_KEY
from t6_grounding.user_service_client import UserServiceClient

#TODO:
# Define SYSTEM_PROMPT - instructs the LLM to act as a RAG-powered assistant:
#   - The user message contains two sections: RAG CONTEXT and USER QUESTION
#   - Answer ONLY based on the provided RAG CONTEXT and conversation history
#   - If no relevant information exists in RAG CONTEXT, state that the question cannot be answered
SYSTEM_PROMPT = None

#TODO:
# Define USER_PROMPT template with two placeholders:
#   - {context} - the retrieved user data
#   - {query}   - the user's question
USER_PROMPT = None


def format_user_document(user: dict[str, Any]) -> str:
    #TODO:
    # - Build a string starting with "User:\n"
    # - For each key-value pair in the user dict, add an indented "  key: value\n" line
    # - Add a blank line at the end
    # - Return the formatted string
    raise NotImplementedError


class UserRAG:
    def __init__(self, embeddings: OpenAIEmbeddings):
        self.embeddings = embeddings
        self._llm_client = OpenAI(api_key=OPENAI_API_KEY)
        self.vectorstore = None

    async def __aenter__(self):
        #TODO:
        # - Print "🔎 Loading all users..."
        # - Fetch all users via UserServiceClient().get_all_users()
        # - Print f"Formatting {len(users)} user documents..."
        # - Create a list of Document objects, each with page_content=format_user_document(user)
        # - Print f"↗️ Creating embeddings and vectorstore for {len(documents)} documents..."
        # - Call await self._create_vectorstore_with_batching(documents, batch_size=100)
        #   and assign the result to self.vectorstore
        # - Print "✅ Vectorstore is ready."
        # - Return self
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _create_vectorstore_with_batching(self, documents: list[Document], batch_size: int = 100):
        #TODO:
        # - Split documents into batches of batch_size using list slicing
        # - Create a list of FAISS.afrom_documents(batch, self.embeddings) coroutines for each batch
        # - Run all coroutines IN PARALLEL using asyncio.gather(..., return_exceptions=True)
        # - Iterate over batch results:
        #   - If final_vectorstore is None, set it to the current batch result
        #   - Otherwise, call final_vectorstore.merge_from(batch_vectorstore) to combine them
        # - If final_vectorstore is still None after all batches, raise Exception("All batches failed to process")
        # - Return the final merged vectorstore
        raise NotImplementedError

    async def retrieve_context(self, query: str, k: int = 10, score: float = 0.1) -> str:
        print("Retrieving context...")
        #TODO:
        # - Call self.vectorstore.similarity_search_with_relevance_scores(query, k=k, score_threshold=score)
        # - Iterate over (doc, relevance_score) pairs:
        #   - Append doc.page_content to context_parts
        #   - Print f"Retrieved (Score: {relevance_score:.3f}): {doc.page_content}"
        # - Print a separator line of 100 "=" characters followed by "\n"
        # - Return all context_parts joined with "\n\n"
        raise NotImplementedError

    def augment_prompt(self, query: str, context: str) -> str:
        #TODO:
        # - Return USER_PROMPT formatted with context and query
        raise NotImplementedError

    def generate_answer(self, augmented_prompt: str) -> str:
        #TODO:
        # - Build a messages list with SYSTEM_PROMPT as system and augmented_prompt as user
        # - Call self._llm_client.chat.completions.create with model='gpt-4o-mini', temperature=0.0
        # - Return the response content string (default to "" if None)
        raise NotImplementedError


async def main():
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small',
        api_key=OPENAI_API_KEY,
        dimensions=384,
    )

    async with UserRAG(embeddings) as rag:
        print("Query samples:")
        print(" - I need user emails that filled with hiking and psychology")
        print(" - Who is John?")
        while True:
            user_question = input("> ").strip()
            if user_question.lower() in ['quit', 'exit']:
                break

            #TODO:
            # - Call await rag.retrieve_context(user_question) and store in context
            # - Call rag.augment_prompt(user_question, context) and store in augmented_prompt
            # - Call rag.generate_answer(augmented_prompt) and print the answer
            raise NotImplementedError


asyncio.run(main())

# The problems with Vector based Grounding approach are:
#   - In current solution we fetched all users once, prepared Vector store (Embed takes money) but we didn't play
#     around the point that new users added and deleted every 5 minutes. (Actually, it can be fixed, we can create once
#     Vector store and with new request we will fetch all the users, compare new and deleted with version in Vector
#     store and delete the data about deleted users and add new users).
#   - Limit with top_k (we can set up to 100, but what if the real number of similarity search 100+?)
#   - With some requests works not so perfectly. (Here we can play and add extra chain with LLM that will refactor the
#     user question in a way that will help for Vector search, but it is also not okay in the point that we have
#     changed original user question).
#   - Need to play with balance between top_k and score_threshold
# Benefits are:
#   - Similarity search by context
#   - Any input can be used for search
#   - Costs reduce