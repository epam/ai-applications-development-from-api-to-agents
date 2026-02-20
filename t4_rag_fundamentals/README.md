# RAG (Retrieval-Augmented Generation) Implementation

A Python implementation task to build a complete RAG system for microwave manual assistance using LangChain, FAISS, and OpenAI

---

## Understanding the RAG Pipeline

Your implementation will demonstrate the complete RAG workflow:

1. **🔍 Retrieval**: Find relevant chunks from the microwave manual based on user query
2. **🔗 Augmentation**: Combine retrieved context with user question in a structured prompt
3. **🤖 Generation**: Use LLM to generate accurate answer based on the provided context

## Application diagram:

![](application-diagram.png)

---

## Task

### If the task in the main branch is hard for you, then switch to the `main-detailed` branch

- OpenAI Documentation: https://developers.openai.com/api/docs/guides/embeddings
- Langchain OpenAI Embeddings Documentation: https://docs.langchain.com/oss/python/integrations/text_embedding/openai
- Langchain OpenAI Chat Documentation: https://docs.langchain.com/oss/python/integrations/chat/openai
- Langchain FAISS Documentation: https://docs.langchain.com/oss/python/integrations/vectorstores/faiss
- Langchain RecursiveCharacterTextSplitter Documentation: https://docs.langchain.com/oss/python/integrations/splitters

Complete the implementation in [app.py](app.py) by filling in all the TODO sections:

### 🔍 **Step 1: Vector Store Setup (`_setup_vectorstore` method)**
- Check if FAISS index already exists locally
- Load existing index or create new one
- Handle both scenarios properly

### 📖 **Step 2: Document Processing (`_create_new_index` method)**
- Load the [microwave_manual.txt](microwave_manual.txt) text file
- Split documents into chunks using RecursiveCharacterTextSplitter
- Create FAISS vector store from document chunks
- Save the index locally for future use

### 🔎 **Step 3: Context Retrieval (`retrieve_context` method)**
- Implement similarity search with relevance scores
- Extract and format relevant document chunks
- Return formatted context for the LLM
> You can experiment with these parameters in the `retrieve_context` method:

> `k`: Number of relevant chunks to retrieve

> `score`: Similarity threshold for chunk relevance
 
>`chunk_size`: Size of document chunks

>`chunk_overlap`: Overlap between chunks

### 🔗 **Step 4: Prompt Augmentation (`augment_prompt` method)**
- Format the user prompt with retrieved context
- Structure the prompt according to the RAG template

### 🤖 **Step 5: Answer Generation (`generate_answer` method)**
- Create proper message structure for the LLM
- Call OpenAI to generate the final answer
- Return the generated response

### ⚙️ **Step 6: Main Configuration**
- Set up OpenAI embeddings client
- Configure the chat completion client
- Initialize the RAG system with proper parameters

---

## Testing Your Implementation

### Valid request samples:
```
What is the maximum cooking time that can be set on microwave?
```
```
What are the steps to set the clock time on the microwave?
```
```
What is the ECO function on this microwave and how do you activate it?
```
```
What should you do if food in plastic or paper containers starts smoking during heating?
```
```
What is the recommended procedure for removing odors from the microwave oven?
```

### Invalid request samples:
```
What do you know about the DIALX Community?
```
```
What do you think about the dinosaur era? Why did they die?
```
