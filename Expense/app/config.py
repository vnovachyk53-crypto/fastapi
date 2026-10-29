from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="MYSQL_", extra="ignore"
    )

    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "expenses_tracker"
    user: str
    password: SecretStr = Field(min_length=3)


@lru_cache
def get_settings() -> Setting:
    return Setting()
