from functools import lru_cache  # кеш: Settings створюється лише один раз

from pydantic import (  # Field — обмеження; SecretStr — не світить пароль у логах
    Field,
    SecretStr
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL  # конструктор URL підключення до БД


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",  # шлях відносно поточної теки запуску (корінь проєкту)
        env_file_encoding="utf-8",
        extra="ignore" # зайві змінні в .env не викликають помилку
    )

    # Параметри підключення до MySQL (окремо, а не одним рядком).
    db_user: str = "app_user"
    db_password: SecretStr = SecretStr(
        "app_password"
    )  # SecretStr: не світиться в repr/логах
    db_host: str = "localhost"
    db_port: int = Field(default=3306, gt=0, lt=65536)
    db_name: str = "auth_demo"

    @property
    def database_url(self) -> URL:
        """Збирає URL: mysql+pymysql://<user>:<password>@<host>:<port>/<db>?charset=utf8mb4.

        URL.create сам екранує спецсимволи в паролі (@, :, / тощо).
        charset=utf8mb4 — повна підтримка Unicode (кирилиця, символи).
        """
        return URL.create(
            drivername="mysql+pymysql",
            username=self.db_user,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": "utf8mb4"}
        )

    # Ім'я cookie, у якому браузер носить ідентифікатор сесії.
    cookie_name: str = "session_id"

    # Скільки секунд браузер зберігає cookie (3600 = 1 година).
    # Увага: у цій простій версії це лише рекомендація браузеру;
    # сервер термін дії сам не перевіряє (це робиться в «професійній» презентації).
    cookie_max_age: int = Field(default=3600, gt=0)

    # Прапорець Secure: cookie надсилається лише через HTTPS.
    # Локально (http://localhost) вимкнено; у production виставте COOKIE_SECURE=true.
    cookie_secure: bool = False


@lru_cache
def get_settings() -> Settings:
    """Повертає єдиний екземпляр налаштувань (зручно підміняти в тестах)."""
    return Settings()


settings = get_settings()
