from fastapi import APIRouter, HTTPException, Query
from typing import List
from services.generation_service import generate_response
from services.retrieval_service import retrieve_top_k_documents
from models.document import RetrievedDocument
import os

router = APIRouter()

# Reuse your database configuration
db_config = {
    "dbname": os.environ.get("POSTGRES_DB"), 
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT")
}

@router.get("/generate")
async def generate_answer_endpoint(
    query: str = Query(..., description="The query text from the user"),
    top_k: int = Query(5, description="Number of top documents to retrieve"),
    max_tokens: int = Query(200, description="The maximum number of tokens to generate"),
    temperature: float = Query(0.7, description="Sampling temperature for the model")
):
    """
    Retrieve the top K relevant documents and generate a response based on them.
    
    Args:
        query (str): The query text from the user.
        top_k (int): Number of top documents to retrieve.
        max_tokens (int): Maximum number of tokens to generate in the response.
        temperature (float): Temperature setting for the generation model.
        
    Returns:
        str: The generated answer based on the query and retrieved documents.
    """
    try:
        # Retrieve documents
        documents = retrieve_top_k_documents(query, top_k, db_config=db_config)
        if not documents:
            raise HTTPException(status_code=404, detail="No documents found.")

        # Pass the RetrievedDocument objects directly
        generated_response = await generate_response(query, documents, max_tokens, temperature) # is this sync?
        return {"response": generated_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")