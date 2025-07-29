# properties_service/app/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = "dev"
    DATABASE_URL: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
