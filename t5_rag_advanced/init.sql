-- Enable the pgvector extension to support vector operations in PostgreSQL
-- This adds vector data type and similarity search functions
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table to store vectors with vector embeddings
-- Each item has an ID, document_name, text, and a 1536-dimensional vector
-- The vector dimension (384) matches common embedding models like OpenAI's
CREATE TABLE IF NOT EXISTS vectors
(
    id            SERIAL PRIMARY KEY,
    document_name VARCHAR(64),
    text          TEXT NOT NULL,
    embedding     VECTOR(384)
);

-- Grant database access permissions to the postgres user
-- This allows the default user to perform all operations on the database
GRANT ALL PRIVILEGES ON DATABASE vectordb TO postgres;
-- Grant table access permissions to the postgres user
-- This allows operations like SELECT, INSERT, UPDATE on all tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
-- Grant sequence access permissions to the postgres user
-- This allows the user to use auto-incrementing IDs in the tables
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- HNSW Index for Euclidean Distance (L2)
-- HNSW generally provides better query performance than IVFFlat
-- m=16: Number of bidirectional links for each node (higher = better recall, more memory)
-- ef_construction=64: Size of dynamic candidate list during index construction (higher = better quality, slower build)
CREATE INDEX IF NOT EXISTS vectors_embedding_l2_hnsw_idx
    ON vectors USING hnsw (embedding vector_l2_ops)
    WITH (m = 16, ef_construction = 64);

-- HNSW Index for Cosine Distance
-- Use this index when performing cosine similarity searches
-- Same parameters as L2 index for consistency
CREATE INDEX IF NOT EXISTS vectors_embedding_cosine_hnsw_idx
    ON vectors USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Example of how to insert data with embeddings (commented for reference)
-- In production, embeddings would be generated from text using AI models
-- INSERT INTO vectors (document_name, text, embedding) VALUES ('microwave.txt', 'This is a test data', '[0.1, 0.2, 0.3, ...]');