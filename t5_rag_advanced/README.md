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
