# RAG (Retrieval-Augmented Generation) Advanced

A Python implementation task to build a complete RAG system for microwave manual assistance using PostgreSQL with pgvector extension and OpenAI API

## Learning Goals

By completing this task, you will learn:
- How to implement the complete RAG pipeline: **Retrieval**, **Augmentation**, and **Generation**
- How to work with vector embeddings and similarity search using PostgreSQL with pgvector
- How to process and chunk text documents for vector storage
- How to perform semantic search with cosine and Euclidean distance metrics
- Understanding RAG architecture without high-level frameworks

---

## Implementation Details

### Database Schema
The PostgreSQL database uses the pgvector extension with this schema:
```sql
CREATE TABLE vectors (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(64),
    text TEXT NOT NULL,
    embedding VECTOR(384)
);
```

### Similarity Search
The system supports two distance metrics:
- **Cosine Distance** (`<=>` operator): Measures angle between vectors
- **Euclidean Distance** (`<->` operator): Measures straight-line distance

### Configuration Parameters
Experiment with these parameters for optimal performance:
- `chunk_size`: Size of text chunks (default: 150, recommended: 300)
- `overlap`: Character overlap between chunks (default: 40)
- `top_k`: Number of relevant chunks to retrieve (default: 5)
- `min_score`: Similarity threshold (range: 0.1-0.99, default: 0.5)
- `dimensions`: Embedding dimensions (1536 for OpenAI models)

---

## Task

### If the task in the main branch is hard for you, then switch to the `main-detailed` branch

Complete the implementation by filling in all the TODO sections across these files:

### **Step 1: Run [docker-compose.yml](docker-compose.yml) with PGVector**
- Check the [init.sql](init.sql) with configuration
- Connect to database:
  - Host: `localhost`
  - Port: `5433` (Pay attention that port is not `5432` standard, it is done to avoid possible conflicts)
  - URL: `postgres`
  - Password: `postgres`
- While testing the application you can check what is inside the DB

### **Step 2: Embeddings Client [embeddings_client.py](embeddings/embeddings_client.py)**
- Complete the `get_embeddings()` method to call embeddings API
- Parse the response and extract embeddings data
- Handle the request/response format according to API specification

### **Step 3: Text Processing [text_processor.py](embeddings/text_processor.py)**
- Implement `process_text_file()` to load, chunk, and store document embeddings
- Complete `_truncate_table()` for database cleanup
- Implement `_save_chunk()` to store text chunks with embeddings in PostgreSQL
- Complete `search()` method for semantic similarity search using pgvector

### **Step 4: Main Application [app.py](app.py)**
- Initialize clients with proper model deployments
- Implement document processing workflow
- Complete the RAG pipeline: Retrieval → Augmentation → Generation
- Handle user interaction and conversation management

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

---

## Additional Experiments

These experiments are designed to deepen your understanding of vector databases and embedding models by intentionally breaking things in instructive ways.

### Experiment 1: Dimension Mismatch

> **Question**: What happens when the database contains embeddings with 384 dimensions, but you search using an embedding with 385 dimensions?

**Steps:**
1. Load context into the database normally (answer `y`, dimensions stay at `384`)
2. In `app.py`, find the `text_processor.search(...)` call and change `dimensions=384` to `dimensions=385`
3. Run the application again, skip loading context (answer `n`), and enter any query

<details> 
<summary><b>Expected result</b></summary>

PgVector will raise an error because the stored vectors have 384 dimensions while the query vector has 385,
dimensions must match exactly for similarity search to work. This shows that a vector database is not just a key-value store; 
the dimensionality of the data is part of the schema.

</details>

---

### Experiment 2: Embedding Model Mismatch

> **Question**: What happens when you use `text-embedding-3-small` for context generation but `nomic-embed-text` for search (both produce 384-dimensional vectors)?

#### Step 1: Add Ollama services to [docker-compose.yml](docker-compose.yml)

Append the two services below inside the `services:`

```yaml
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped

  ollama-init:
    image: ollama/ollama:latest
    depends_on:
      - ollama
    entrypoint: >
      /bin/sh -c "sleep 5 && ollama pull nomic-embed-text"
    environment:
      - OLLAMA_HOST=http://ollama:11434
    restart: "no"
```

and add `ollama_data:` to the `volumes:` block:

```yaml
volumes:
  rag-advanced-task:
  ollama_data:
```

**Pay attention that *ollama* is quite heavy image ~4GB**

#### Step 2: Start all services and pull the model

```bash
docker compose down && docker compose up -d
```

`ollama-init` will automatically pull `nomic-embed-text` after Ollama starts.

#### Step 3: Load context using OpenAI `text-embedding-3-small`

Keep the original `embeddings_client` (pointing to OpenAI). Run the app and answer `y` to load context, embeddings are stored with `text-embedding-3-small`.

#### Step 4: Switch `embeddings_client` to Ollama in `app.py`

Replace the `embeddings_client` instantiation with:

```python
embeddings_client = EmbeddingsClient(
    endpoint="http://localhost:11434/v1/embeddings",
    model_name='nomic-embed-text',
    api_key="ollama"
)
```

#### Step 5: Run the app again without reloading context

Answer `n` when asked to load context, then enter a query.

<details> 
<summary><b>Expected result</b></summary>

Even though both models produce 384-dimensional vectors, the similarity search will return poor or irrelevant results. 
`text-embedding-3-small` and ollama `nomic-embed-text` encode text into completely different vector spaces, comparing 
their outputs is geometrically meaningless. This demonstrates why **embedding model consistency between indexing and querying is critical** in every RAG system.

</details>