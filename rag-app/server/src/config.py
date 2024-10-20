from pydantic import BaseSettings


class Settings(BaseSettings):
    # Define your configuration fields here with optional defaults
    environment: str = "dev"
    app_name: str = "Oxford GenAI Capstone"
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"  # Load variables from .env if they exist
