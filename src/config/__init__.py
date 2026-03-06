"""Application settings via pydantic-settings."""

from enum import StrEnum
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    """Settings loaded from environment and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    # core
    env: Annotated[Env, Field(description="Application environment", default=Env.PROD)]
    debug: Annotated[bool, Field(description="Enable debug mode", default=False)]
    # db
    db_schema: Annotated[str, Field(description="Database schema", default="")]
    db_host: Annotated[str, Field(description="Database host", default="")]
    db_port: Annotated[int, Field(description="Database port", default=0)]
    db_name: Annotated[str, Field(description="Database name", default="")]
    db_user: Annotated[str, Field(description="Database user", default="")]
    db_password: Annotated[str, Field(description="Database password", default="")]


settings = Settings()
