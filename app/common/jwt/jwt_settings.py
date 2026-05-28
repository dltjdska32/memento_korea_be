from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env",  env_file_encoding="utf-8")

    jwt_secret: str
    jwt_access_exp: int = 1800000  # default - 30분
    jwt_refresh_exp: int = 604800000  # default - 1주. , 2주 - 1209600000
    jwt_algorithm: str

jwt_settings = JwtSettings()