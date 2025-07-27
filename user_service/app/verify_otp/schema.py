# user_service/app/verify_otp/schema.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class VerifyOtpRequest(BaseModel):
    phone_number: str
    otp: str

class UserInfo(BaseModel):
    id: UUID  # ✅ fix: was int before
    fullname: str
    phone_number: str

class TokenResponse(BaseModel):
    access_token: Optional[str] = None
    message: str
    user: Optional[UserInfo] = None
