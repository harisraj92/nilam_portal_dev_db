from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FRONTEND_ORIGIN: str = "" 

    # Database
    DATABASE_URL: str

    # Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
