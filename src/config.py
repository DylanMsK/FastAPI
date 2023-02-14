import configparser
from functools import lru_cache

from pydantic import BaseModel, BaseSettings, PostgresDsn

from src.constants import Environment


config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")


class AppConfig(BaseModel):
    title: str = config["DEFAULT"]["TITLE"]
    version: str = config["DEFAULT"]["VERSION"]
    description: str = config["DEFAULT"]["DESCRIPTION"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GlobalSettings(BaseSettings):
    APP_CONFIG: AppConfig = AppConfig()
    ENVIRONMENT: Environment = Environment.LOCAL


class DevelopmentSettings(GlobalSettings):
    SITE_DOMAIN: str
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = "dev.env"


class ProductionSettings(GlobalSettings):
    SITE_DOMAIN: str
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = "prod.env"


@lru_cache()
def get_settings():
    settings = GlobalSettings()
    if settings.ENVIRONMENT.is_debug:
        return DevelopmentSettings(**settings.dict())
    return ProductionSettings(**settings.dict())


settings = get_settings()
