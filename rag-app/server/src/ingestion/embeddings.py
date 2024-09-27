from sentence_transformers import SentenceTransformer
from typing import List

# Load a pre-trained Sentence Transformer model (e.g., 'all-MiniLM-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text: str, max_length: int = 512) -> List[str]:
    """
    Chunk the text into smaller pieces based on the max token length.
    
    Args:
        text (str): The text to chunk.
        max_length (int): The maximum length of each chunk.
        
    Returns:
        List[str]: A list of text chunks.
    """
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    
    # Add the remaining chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def generate_embeddings(text_chunks: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of text chunks.
    
    Args:
        text_chunks (List[str]): The list of text chunks.
        
    Returns:
        List[List[float]]: A list of embeddings (one embedding per chunk).
    """
    embeddings = model.encode(text_chunks, convert_to_tensor=False)
    return embeddings