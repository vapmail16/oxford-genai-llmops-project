from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Define your configuration fields here with optional defaults
    environment: str = Field(..., env="ENVIRONMENT")
    app_name: str = Field(..., env="APP_NAME")
    debug: bool = Field(..., env="DEBUG")

    # database config
    # database_url: str = Field(..., env="DATABASE_URL")
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: int = 5432  # default
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")

    # ingestion config
    arxiv_api_url: str = Field(..., env="ARXIV_API_URL")
    data_path: str = Field(..., env="DATA_PATH")

    # Evidently config
    evidently_api_key: str = Field(..., env="EVIDENTLY_API_KEY")
    evidently_team_id: str = Field(..., env="EVIDENTLY_TEAM_ID")
    evidently_dataset_name: str = Field(..., env="EVIDENTLY_DATASET_NAME")
    evidently_address: str = Field(..., env="EVIDENTLY_ADDRESS")

    # LLM Service Config
    ollama_api_url: str = Field(..., env="OLLAMA_API_URL")
    ollama_model: str = Field(..., env="GENERATOR_MODEL")
    ollama_streaming: bool = Field(..., env="OLLAMA_STREAMING")

    class Config:
        env_file = ".env"  # Load variables from .env if they exist


settings = Settings()
