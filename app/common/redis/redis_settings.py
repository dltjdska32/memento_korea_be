from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    redis_host: str
    redis_port: int = 6379
    redis_password: str
    redis_db: int

    @property
    def redis_url(self):
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


redis_settings = RedisSettings()


