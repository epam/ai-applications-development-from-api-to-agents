# AI Grounding

A comprehensive Python implementation demonstrating different approaches to grounding AI systems with external data sources.
This task explores three distinct grounding strategies for user search and retrieval systems.

## Learning Goals

By exploring this project, you will learn:
- Different approaches to AI grounding: **No Grounding**, **Input Grounding**, and **Input-Output Grounding**
- How to implement vector-based similarity search using FAISS and Chroma
- API-based data retrieval and search parameter extraction
- Token optimization strategies and cost management
- Trade-offs between accuracy, performance, and cost in AI systems

---

## Task

### 0. Run [docker-compose.yml](docker-compose.yml)
The mock user service runs on `localhost:8041` and provides:
- `/v1/users` - Get all users
- `/v1/users/{id}` - Get specific user
- `/v1/users/search` - Search users by fields
- `/health` - Service health check
- Swagger UI 👉 http://localhost:8041/docs

---

### 1. No Grounding — [t1/no_grounding.py](t1/no_grounding.py)
Direct LLM processing without external knowledge integration.

Open [t1/no_grounding.py](t1/no_grounding.py) and explore how it works:
- Loads all users into context
- Processes user batches in parallel
- Combines results for final answer

**Pros:** Simple implementation, no external dependencies
**Cons:** High token usage and costs, context window limitations, risk of data modification through LLM processing

---

### 2. Input-based Grounding — [t2](t2)

#### API-based — [t2/input_api_based.py](t2/input_api_based.py)
Open [t2/input_api_based.py](t2/input_api_based.py) and explore how it works:
- Analyzes query to extract search fields (name, surname, email) using structured output
- Makes targeted API calls with specific parameters
- Returns exact matches from live data

**Pros:** Real-time data access, cost-efficient for exact matches, no embedding overhead
**Cons:** Requires exact parameter matching, less flexible than semantic search, additional LLM call for parameter extraction

#### Vector-based — [t2/input_vector_based.py](t2/input_vector_based.py)
Open [t2/input_vector_based.py](t2/input_vector_based.py) and explore how it works:
- Creates vector embeddings for all users
- Performs similarity search using FAISS
- Retrieves top-k most relevant users

**Pros:** Semantic understanding, flexible search queries, reduced API costs
**Cons:** Static data (needs manual refresh), top-k limitations, embedding costs

---

### 3. Input-Output Grounding — [t3/in_out_grounding.py](t3/in_out_grounding.py)
Combines vector search with structured output and real-time data retrieval.

Open [t3/in_out_grounding.py](t3/in_out_grounding.py) and explore how it works:
- Uses Chroma vector store for semantic similarity filtering
- Structures LLM output with Pydantic models and `response_format`
- Fetches live user data for final results (Output Grounding)
- Auto-updates vector store with new/deleted users

**Pros:** Best of both worlds — semantic search + live data, structured parseable outputs, automatic data synchronization
**Cons:** Most complex implementation, higher computational overhead

---

**Congratulations 🎉 You now understand the trade-offs between No Grounding, Input Grounding, and Input-Output Grounding approaches!**