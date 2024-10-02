/* Create the vector extension */
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE papers (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    chunk TEXT NOT NULL,
    embedding vector(384)  -- Adjust to match the embedding dimension (384 for all-MiniLM-L6-v2)
);

/*
CREATE TABLE IF NOT EXISTS embeddings (
  id SERIAL PRIMARY KEY,
  embedding vector,
  text text,
  created_at timestamptz DEFAULT now()
);]
*/