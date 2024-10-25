"""
This is the main entry point for the backend application, this will define and instantiate the FastAPI server
that uses the controllers, models and services defined in the rest of the sub-repo.

For development purposes this will run on localhost:8000
"""

# server/src/main.py
from fastapi import FastAPI, Depends
from controllers import retrieval, health_check, generation

# from server.src.config_loader import ConfigLoader
from server.src.config import Settings
import os

app = FastAPI()

# Include routers
app.include_router(retrieval.router)
app.include_router(health_check.router)
app.include_router(generation.router)

# Define a fastAPI dependency provider
# def get_settings():
#     return Settings()


# @app.get("/config")
# async def get_config(settings: Settings = Depends(get_settings)):
#     return {
#         "environment": settings.environment,
#         "app_name": settings.app_name,
#         "debug": settings.debug,
#         "database_url": settings.database_url,
#     }


@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG app!"}
