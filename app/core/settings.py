from functools import lru_cache
from typing import Any
from pydantic import BaseSettings, SecretStr, validator

class Settings(BaseSettings):
    title: str = "Stats-service"
    descriprion: str = "Service for displaying statistics for a specific search query on Wildberries"
    parse_url: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_db: str
    postgres_uri: str | None = None
    
    
    @validator("postgres_uri", pre=True)
    def validate_postgres_uri(cls, v: str | None, values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        password: SecretStr = values.get("postgres_password", SecretStr(""))
        return "{scheme}://{user}:{password}@{host}/{db}".format(
            scheme="postgresql+asyncpg",
            user=values.get("postgres_user"),
            password=password.get_secret_value(),
            host=values.get("postgres_host"),
            db=values.get("postgres_db"),
        )

    class Config:
        env_file = '.env.dev'

@lru_cache()
def get_settings(**kwargs):
    return Settings(**kwargs)