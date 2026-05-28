
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Memento Korea"
    debug: bool = True
    env: str = "local"   # local, dev, prod


settings = Settings()