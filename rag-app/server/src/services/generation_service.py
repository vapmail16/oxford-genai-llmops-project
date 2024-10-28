import boto3
import os
from typing import List, Dict
from models.document import RetrievedDocument  # Import the Pydantic model
from server.src.config import Settings
from fastapi import Depends
import requests
import json

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
prompt_data = {"model": "tinyllama", "stream": False}


async def generate_response(
    query: str,
    chunks: List[Dict],
    max_tokens: int = 200,
    temperature: float = 0.7,
) -> str:
    """
    Generate a response using an Ollama endpoint running locally, t
    his will be changed to allow for Bedrock later.

    Args:
        query (str): The user query.
        context (List[Dict]): The list of documents retrieved from the retrieval service.
        max_tokens (int): The maximum number of tokens to generate in the response.
        temperature (float): Sampling temperature for the model.
    """
    QUERY_PROMPT = """
    You are a helpful AI language assistant, please use the following context to answer the query.
    Context: {context}
    Query: {query}
    Answer:
    """
    # Concatenate documents' summaries as the context for generation
    context = "\n".join([chunk["chunk"] for chunk in chunks])
    prompt = QUERY_PROMPT.format(context=context, query=query)
    prompt_data["prompt"] = prompt
    # print(prompt_data)
    response = requests.post(url, headers=headers, data=json.dumps(prompt_data))
    if response.status_code == 200:
        print("Succesfully generated response")
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        print(actual_response)
        return actual_response
    else:
        print(f"Error hitting Ollama: {response.status_code} - {response.text}")
        return None  # TODO: error handling


# # Initialize the Bedrock client
# def get_bedrock_client():
#     """
#     Initialize and return the Bedrock client using boto3.
#     """
#     return boto3.client(
#         "bedrock-runtime",  # This service name may change based on AWS SDK updates
#         region_name=os.environ.get("AWS_REGION", "us-east-1"),
#     )


# def get_llm_client(settings=Depends(get_settings)):
#     """
#     Initiatlise and return client for given LLM provider.
#     """
#     return None


# async def generate_response(
#     query: str,
#     documents: List[RetrievedDocument],
#     max_tokens: int = 200,
#     temperature: float = 0.7,
# ) -> str:
#     """
#     Generate a response using Amazon Bedrock based on the query and retrieved documents.

#     Args:
#         query (str): The user query.
#         documents (List[RetrievedDocument]): The list of documents retrieved from the retrieval service.
#         max_tokens (int): The maximum number of tokens to generate in the response.
#         temperature (float): Sampling temperature for the model.

#     Returns:
#         str: The generated response from the model.
#     """
#     # Create a Bedrock client
#     client = get_bedrock_client()

#     # Concatenate documents' summaries as the context for generation
#     context = "\n".join([doc.summary for doc in documents])

#     # Define the model prompt
#     prompt = f"Based on the following information:\n{context}\n\nAnswer the following question:\n{query}"

#     try:
#         # Call Amazon Bedrock's InvokeModel API
#         response = client.invoke_model(
#             modelId="amazon/bedrock-language-model",  # Replace with the correct model ID for your setup
#             body={
#                 "input": prompt,
#                 "max_tokens": max_tokens,
#                 "temperature": temperature,
#             },
#         )

#         # Retrieve and return the generated text
#         result = response["body"]["generated_text"]
#         return result

#     except Exception as e:
#         print(f"Error generating response: {e}")
#         raise e
