from pydantic_settings import BaseSettings
from typing import Optional
class Settings(BaseSettings):
    # OpenAI and LangFuse settings
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()