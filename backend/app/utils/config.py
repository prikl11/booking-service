from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    model_config = {"env_file": ".env"}

settings = Settings()