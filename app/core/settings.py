from functools import lru_cache
from typing import Any
from pydantic import BaseSettings, SecretStr, validator


class Settings(BaseSettings):
    title: str = "Stats-service"
    descriprion: str = "Service for displaying statistics for \
        a specific search query on Wildberries"

    # Database
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_db: str
    postgres_uri: str | None = None

    # Parser
    parse_timeout: int = 1  # minutes as default
    parse_url: str

    # Worker
    worker_host: str
    worker_port: int
    worker_socket: str = None

    @validator("postgres_uri", pre=True)
    def validate_postgres_uri(
        cls, v: str | None, values: dict[str, Any]
    ) -> str:
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

    @validator("worker_socket", pre=True)
    def validate_worker_socket(
        cls, v: str | None, values: dict[str, Any]
    ) -> str:
        if isinstance(v, str):
            return v
        return f"{values.get('worker_host')}:{values.get('worker_port')}"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings(**kwargs):
    return Settings(**kwargs)
