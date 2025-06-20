from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    twilio_account_sid: str = Field(..., alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(..., alias="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(..., alias="TWILIO_PHONE_NUMBER")
    secret_key: str = Field(..., alias="SECRET_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False
        allow_population_by_field_name = True

settings = Settings()
