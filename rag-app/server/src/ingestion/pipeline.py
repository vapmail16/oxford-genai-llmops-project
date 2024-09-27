from arxiv_client import fetch_papers
from embeddings import chunk_text, generate_embeddings
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection configuration
db_config = {
    "dbname": os.environ.get("POSTGRES_DB"), 
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT")
}

def save_to_db(papers, embeddings):
    """
    Save the paper titles, summaries, and embeddings to Postgres.
    
    Args:
        papers (list): A list of papers with titles and summaries.
        embeddings (list): A list of embeddings for the corresponding papers.
    """
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO papers (title, summary, embedding) 
    VALUES %s
    """
    
    # Prepare values for bulk insertion
    values = [
        (paper['title'], paper['summary'], embedding.tolist())
        for paper, embedding in zip(papers, embeddings)
    ]
    
    # Bulk insert
    execute_values(cursor, insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()

def run_ingestion_pipeline(query: str, max_results: int = 10):
    """
    Main function to run the ingestion pipeline.
    
    Args:
        query (str): The query to search papers on arXiv.
        max_results (int): The maximum number of papers to ingest.
    """
    # Step 1: Fetch papers from arXiv
    papers = fetch_papers(query, max_results)
    
    # Step 2: Chunk summaries and generate embeddings
    all_embeddings = []
    
    for paper in papers:
        chunks = chunk_text(paper['summary'])
        embeddings = generate_embeddings(chunks)
        all_embeddings.append(embeddings)
    
    # Step 3: Save papers and embeddings to the database
    save_to_db(papers, all_embeddings)
    print(f"Successfully ingested {len(papers)} papers.")

if __name__ == "__main__":
    # Example: Run the pipeline with a query
    run_ingestion_pipeline("machine learning", max_results=10)