# AI Grounding

A comprehensive Python implementation demonstrating different approaches to grounding AI systems with external data sources. This project explores three distinct grounding strategies for user search and retrieval systems.

## 🎯 Learning Goals

By exploring this project, you will learn:
- Different approaches to AI grounding: **No Grounding**, **Input Grounding**, and **Input-Output Grounding**
- How to implement vector-based similarity search using FAISS and Chroma
- API-based data retrieval and search parameter extraction
- Token optimization strategies and cost management
- Trade-offs between accuracy, performance, and cost in AI systems

## 📋 Requirements

- Python 3.11+
- Docker and Docker Compose

## 🔧 Setup

1. **Start the user service:**
   ```bash
   docker-compose up -d
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials:**
    - Set environment variable

## 🏗️ Project Structure

```
task/
├── _constants.py             ✅ API configuration
├── user_client.py            ✅ User service client
├── t1/
│   └── no_grounding.py       🚧 1: No grounding
├── t2/
│   ├── Input_vector_based.py 🚧 2.1: Vector-based input grounding  
│   └── input_api_based.py    🚧 2.2: API-based input grounding
└── t3/
    └── in_out_grounding.py   🚧 3: Input-output grounding
```

## 📊 Grounding Approaches

### If the task in the main branch is hard for you, then switch to the `with-detailed-description` branch

### 1. No Grounding (`t1/no_grounding.py`)
Direct LLM processing without external knowledge integration.

**How it works:**
- Loads all users into context
- Processes user batches in parallel
- Combines results for final answer

**Pros:**
- Simple implementation
- No external dependencies

**Cons:**
- High token usage and costs
- Context window limitations
- Risk of data modification through LLM processing

### 2. Input-based Grounding (`t2/`)

#### Vector-based (`Input_vector_based.py`)
Uses semantic similarity search with embeddings.

**How it works:**
- Creates vector embeddings for all users
- Performs similarity search using FAISS
- Retrieves top-k most relevant users

**Pros:**
- Semantic understanding
- Flexible search queries
- Reduced API costs

**Cons:**
- Static data (needs manual refresh)
- Top-k limitations
- Embedding costs

#### API-based (`input_api_based.py`)
Extracts search parameters and uses structured API calls.

**How it works:**
- Analyzes query to extract search fields
- Makes targeted API calls with specific parameters
- Returns exact matches from live data

**Pros:**
- Real-time data access
- Cost-efficient for exact matches
- No embedding overhead

**Cons:**
- Requires exact parameter matching
- Less flexible than semantic search
- Additional LLM call for parameter extraction

### 3. Input-Output Grounding (`t3/in_out_grounding.py`)
Combines vector search with structured output and real-time data retrieval.

**How it works:**
- Uses vector similarity for initial filtering
- Structures LLM output with Pydantic models
- Fetches live user data for final results
- Auto-updates vector store with new/deleted users

**Pros:**
- Best of both worlds: semantic search + live data
- Structured, parseable outputs
- Automatic data synchronization

**Cons:**
- Most complex implementation
- Higher computational overhead


### User Service
Swagger UI 👉 http://localhost:8041/docs

The mock user service runs on `localhost:8041` and provides:
- `/v1/users` - Get all users
- `/v1/users/{id}` - Get specific user
- `/v1/users/search` - Search users by fields
- `/health` - Service health check
