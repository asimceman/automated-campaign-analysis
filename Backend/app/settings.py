import os
import urllib
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    # PostgreSQL
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str

    # LLM
    OPEN_AI_URL: str
    OPENAI_API_KEY: str

    # Mailgun
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str
    RECIPIENT_EMAIL: str

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{urllib.parse.quote(self.DB_PASSWORD)}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        extra = "ignore"

settings = Settings(_env_file=os.environ.get("ENV_FILE", ".env"))