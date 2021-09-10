from pydantic import BaseSettings


class Config(BaseSettings):
    """Объект настроек для приложения"""

    HUB_HOST: str
    """Хост для селениума"""


settings = Config()
