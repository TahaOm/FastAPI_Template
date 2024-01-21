import os
from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings

"""Load the environment file"""
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")


class Settings(BaseSettings):
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT")
    API_VERSION: str = os.environ.get("API_VERSION")
    PROJECT_NAME: str = os.environ.get("PROJECT_NAME")
    FILE_VOLUME: str = os.environ.get("FILE_VOLUME")
    TEMPLATES_DIR: str
    EMAIL_TEMPLATES_DIR: str

    if not os.path.exists(FILE_VOLUME):
        os.makedirs(FILE_VOLUME)

    # SERVER_HOST: AnyHttpUrl
    # SENTRY_DSN: Optional[HttpUrl] = None

    # BACKEND_CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "").split(",")
    BACKEND_CORS_ORIGINS: List[str] = [os.getenv("CORS_ORIGINS")]

    # mail config
    MAIL_FROM: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int


class DevConfig(Settings):
    """Development configurations."""

    pass


class TestConfig(Settings):
    """Production configurations."""

    pass


class ProdConfig(Settings):
    """Production configurations."""

    pass


class FactoryConfig:
    """Returns a config instance dependence on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "development":
            return DevConfig()

        elif self.env_state == "production":
            return ProdConfig()

        elif self.env_state == "testing":
            return TestConfig()


@lru_cache()
def get_configs():
    return FactoryConfig(Settings().ENVIRONMENT)()


# Create an instance of the Settings class
settings = get_configs()
