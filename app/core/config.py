from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str

    # OpenAI (NEW — REQUIRED)
    openai_api_key: str

    model_config = ConfigDict(
        env_file=".env",
        extra="forbid"  # keep strict (GOOD PRACTICE)
    )


settings = Settings()
