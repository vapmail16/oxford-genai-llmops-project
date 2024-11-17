import boto3
from botocore.exceptions import ClientError
import os
from typing import List, Dict, Union
from server.src.models.document import RetrievedDocument  # Import the Pydantic model
from server.src.config import Settings
from fastapi import Depends
import requests
import json
from server.src.config import settings
import opik


@opik.track  # TODO: test if this works with async methods? I think it will.
def call_llm(prompt: str) -> Union[Dict, None]:
    # TODO find a better place for these to live!
    headers = {"Content-Type": "application/json"}
    prompt_data = {
        "model": settings.ollama_model,
        "stream": settings.ollama_streaming,
        "prompt": prompt,
    }
    response = requests.post(
        url=settings.ollama_api_url, headers=headers, data=json.dumps(prompt_data)
    )
    if response.status_code == 200:
        print("Succesfully generated response")
        response_text = response.text
        data = json.loads(response_text)
        data["response_tokens_per_second"] = (
            data["eval_count"] / data["eval_duration"] * 10**9
        )  # https://github.com/ollama/ollama/blob/main/docs/api.md
        data.pop("context")  # don't want to store context yet ...
        return data

    else:
        print(f"Error calling LLM: {response.status_code} - {response.text}")
        return None  # TODO: error handling


def call_bedrock(prompt: str) -> Union[Dict, None]:
    # Create an Amazon Bedrock Runtime client. TODO: can this be a singleton?
    brt = boto3.client("bedrock-runtime")
    # Set the model ID, e.g., Amazon Titan Text G1 - Express.
    model_id = settings.bedrock_model_id

    # Start a conversation with the user message. TODO: Keep conversational context.
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = brt.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={
                "maxTokens": settings.max_tokens,
                "temperature": settings.temperature,
                "topP": settings.top_p,
            },
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)


@opik.track
async def generate_response(
    query: str,
    chunks: List[Dict],
    max_tokens: int = 200,
    temperature: float = 0.7,
) -> Dict:  # str:
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
    You are a helpful AI language assistant, please use the following context to answer the query. Answer in English.
    Context: {context}
    Query: {query}
    Answer:
    """
    # Concatenate documents' summaries as the context for generation
    context = "\n".join([chunk["chunk"] for chunk in chunks])
    prompt = QUERY_PROMPT.format(context=context, query=query)
    response = call_llm(prompt)
    return response  # now this is a dict.


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
