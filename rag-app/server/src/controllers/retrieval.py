from fastapi import APIRouter, HTTPException, Query
from typing import List
from services.retrieval_service import retrieve_top_k_documents
from models.document import Document, RetrievedDocument
from dotenv import load_dotenv
import os

load_dotenv()

DATA_PATH = os.getenv('DATA_PATH')

# Database connection configuration
db_config = {
    "dbname": os.environ.get("POSTGRES_DB"), 
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT")
}

router = APIRouter()

@router.get("/retrieve", response_model=List[RetrievedDocument])
async def retrieve_top_k_documents_endpoint(
    query: str = Query(..., description="The query text from the user"),
    top_k: int = Query(5, description="Number of top documents to retrieve (default is 5)")
):
    """
    Retrieve the top K relevant documents based on a query.
    
    Args:
        query (str): The query text from the user.
        top_k (int): Number of top documents to retrieve (default is 5).
        
    Returns:
        List[Document]: A list of the top retrieved documents.
    """
    try:
        # TODO: Tried using await but retrieve top k is not async, can try adapting to use asyncpg in future.
        documents =  retrieve_top_k_documents(query, top_k, db_config=db_config)
        if not documents:
            raise HTTPException(status_code=404, detail="No documents found.")
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")