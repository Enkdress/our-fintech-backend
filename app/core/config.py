from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "our-fintech-backend"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"


settings = Settings()
