from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "config"


class BootstrapSettings(BaseSettings):
    ENV: Literal["dev", "test", "prod"] = "dev"

    model_config = SettingsConfigDict(
        env_file=CONFIG_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MONGO_URI: str
    MONGO_DB: str

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_RAW_TOPIC: str
    KAFKA_DLQ_TOPIC: str
    KAFKA_CONSUMER_GROUP: str

    CRAWLER_LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


def load_settings() -> Settings:
    bootstrap = BootstrapSettings()

    env_file = CONFIG_DIR / f".env.{bootstrap.ENV}"

    if not env_file.exists():
        raise FileNotFoundError(
            f"Environment file not found: {env_file}"
        )

    return Settings(_env_file=env_file)