import os

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import SecretStr

from commons.constants import OPENAI_API_KEY

_SYSTEM_PROMPT = """You are a RAG-powered assistant that assists users with their questions about microwave usage.
            
## Structure of User message:
`RAG CONTEXT` - Retrieved documents relevant to the query.
`USER QUESTION` - The user's actual question.

## Instructions:
- Use information from `RAG CONTEXT` as context when answering the `USER QUESTION`.
- Cite specific sources when using information from the context.
- Answer ONLY based on conversation history and RAG context.
- If no relevant information exists in `RAG CONTEXT` or conversation history, state that you cannot answer the question.
"""

_USER_PROMPT = """##RAG CONTEXT:
{context}


##USER QUESTION: 
{query}"""


class _MicrowaveRAG:

    def __init__(self, embeddings: OpenAIEmbeddings, llm_client: ChatOpenAI):
        self.llm_client = llm_client
        self.embeddings = embeddings
        self.vectorstore = self._setup_vectorstore()

    def _setup_vectorstore(self) -> VectorStore:
        """
        Load existing FAISS index from disk or create a new one.
        Returns:
              VectorStore: Initialized FAISS vectorstore.
        """
        print("🔄 Initializing Microwave Manual RAG System...")

        if os.path.exists('microwave_faiss_index'):
            vectorstore = FAISS.load_local(
                folder_path='microwave_faiss_index',
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True,
            )
            print("✅ Loaded existing FAISS index")
        else:
            vectorstore = self._create_new_index()
            print("✅ RAG system initialized successfully!")

        return vectorstore

    def _create_new_index(self) -> VectorStore:
        """
        Load the manual, split into chunks, embed, and save a new FAISS index.
        Returns:
              VectorStore: Newly created and saved FAISS vectorstore.
        """
        print("📖 Loading text document...")
        loader = TextLoader('microwave_manual.txt', encoding='utf-8')
        documents = loader.load()

        print("✂️ Splitting document into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            separators=["\n\n", "\n", "."]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")

        print("🔍 Creating embeddings and FAISS index...")
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local("microwave_faiss_index")
        print("💾 Index saved for future use")

        return vectorstore

    def retrieve_context(self, query: str, k: int = 4, score=0.3):
        """
        Retrieve the context for a given query.
        Args:
              query (str): The query to retrieve the context for.
              k (int): The number of relevant documents(chunks) to retrieve.
              score (float): The similarity score between documents and query. Range 0.0 to 1.0.
        """
        print(f"{'=' * 100}\n🔍 STEP 1: RETRIEVAL\n{'-' * 100}")
        print(f"Query: '{query}'")
        print(f"Searching for top {k} most relevant chunks with similarity score {score}:")

        relevant_docs = self.vectorstore.similarity_search_with_relevance_scores(
            query,
            k=k,
            score_threshold=score
        )

        context_parts = []
        for (doc, score) in relevant_docs:
            context_parts.append(doc.page_content)
            print(f"\n--- (Relevance Score: {score:.3f}) ---")
            print(f"Content: {doc.page_content}")

        print("=" * 100)
        return "\n\n".join(context_parts)

    def augment_prompt(self, query: str, context: str):
        """
        Inject retrieved context and user query into the prompt template.
        Args:
              query (str): The user's question.
              context (str): Retrieved context from the vectorstore.
        Returns:
              str: Formatted prompt ready for the LLM.
        """
        print(f"\n🔗 STEP 2: AUGMENTATION\n{'-' * 100}")

        augmented_prompt = _USER_PROMPT.format(context=context, query=query)

        print(f"{augmented_prompt}\n{'=' * 100}")
        return augmented_prompt

    def generate_answer(self, augmented_prompt: str):
        """
        Send the augmented prompt to the LLM and return its response.
        Args:
              augmented_prompt (str): The prompt with injected context and query.
        Returns:
              str: The LLM-generated answer.
        """
        print(f"\n🤖 STEP 3: GENERATION\n{'-' * 100}")

        messages = [
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=augmented_prompt)
        ]

        response = self.llm_client.invoke(messages)

        print(f"{response.content}\n{'=' * 100}")
        return response.content


def main(rag: _MicrowaveRAG):
    print("🎯 Microwave RAG Assistant")

    while True:
        user_question = input("\n> ").strip()
        # Step 1: Retrieval
        context = rag.retrieve_context(user_question) # Here you can play with `k` and similarity score params
        # Step 2: Augmentation
        augmented_prompt = rag.augment_prompt(user_question, context)
        # Step 3: Generation
        answer = rag.generate_answer(augmented_prompt)


main(
    _MicrowaveRAG(
        embeddings=OpenAIEmbeddings(
            model='text-embedding-3-small',
            api_key=SecretStr(OPENAI_API_KEY),
        ),
        llm_client=ChatOpenAI(
            temperature=0.0,
            model='gpt-5.2',
            api_key=SecretStr(OPENAI_API_KEY),
        )
    )
)