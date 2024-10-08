'''
This is the main entry point for the backend application, this will define and instantiate the FastAPI server
that uses the controllers, models and services defined in the rest of the sub-repo.

For development purposes this will run on localhost:8000
'''

# server/src/main.py
from fastapi import FastAPI
from controllers import retrieval, health_check, generation

app = FastAPI()

# Include routers
app.include_router(retrieval.router)
app.include_router(health_check.router)
app.incldue_router(generation.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG app!"}