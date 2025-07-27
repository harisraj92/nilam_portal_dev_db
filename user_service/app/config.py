# user_service/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Runtime Environment
    env: str = "dev"  # dev / prod

    # Database
    database_url: str

    # JWT Auth Settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # OTP Configuration
    otp_length: int = 6
    otp_expiry_seconds: int = 30
    otp_retry_limit: int = 1

    class Config:
        env_file = ".env"     # Load from root .env
        env_file_encoding = "utf-8"

# Export settings instance
settings = Settings()
