from pydantic_settings import BaseSettings
from pydantic import Field

# import os # Used for code that needs testing below.
# import yaml


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

    # Ollama Config
    ollama_api_url: str = Field(..., env="OLLAMA_API_URL")
    ollama_model: str = Field(..., env="GENERATOR_MODEL")
    ollama_streaming: bool = Field(..., env="OLLAMA_STREAMING")

    # Generation model config
    temperature: str = Field(..., env="TEMPERATURE")
    top_p: str = Field(..., env="TOP_P")
    max_tokens: int = Field(..., env="MAX_TOKENS")

    # Bedrock config
    bedrock_model_id: str = Field(..., env="BEDROCK_MODEL_ID")

    # Comet config for Opik
    opik_api_key: str = Field(..., env="OPIK_API_KEY")
    opik_workspace: str = Field(..., env="OPIK_WORKSPACE")
    opik_project_name: str = Field(..., env="OPIK_PROJECT_NAME")

    rag_config: dict = {}

    class Config:
        env_file = ".env"  # Load variables from .env if they exist

    # TODO: Test this
    # @classmethod
    # def load_yaml_config(cls, config_name="rag_flow.yaml"):
    #     """
    #     Loads RAG-specific configuration from a YAML file.
    #     """
    #     config_path = os.path.join(os.path.dirname(__file__), config_name)
    #     with open(config_path, 'r') as file:
    #         return yaml.safe_load(file)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # Load and attach the YAML config
    #     self.rag_config = self.load_yaml_config()


settings = Settings()
