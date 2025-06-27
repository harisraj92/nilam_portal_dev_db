from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.enums import OTPStatusEnum  # ✅ Enum imported

# --- Public API Schemas ---

class OTPRequest(BaseModel):
    """
    Schema to request an OTP using a phone number.
    """
    phone_number: str = Field(..., example="+917010001599")


class OTPVerify(BaseModel):
    """
    Schema to verify a received OTP.
    """
    phone_number: str = Field(..., example="+917010001599")
    otp: str = Field(..., example="123456")


class OTPResponse(BaseModel):
    """
    Standard response schema after sending or verifying an OTP.
    """
    success: bool
    message: str


# --- Internal (DB Logic) Schemas ---

class OTPAttemptCreate(BaseModel):
    """
    Schema for creating an OTP attempt entry in the database.
    """
    phone_number: str
    otp_hash: str
    expires_at: datetime
    last_sent_at: datetime
    status: OTPStatusEnum = OTPStatusEnum.pending


class OTPVerifyAttempt(BaseModel):
    """
    Schema for verifying an OTP attempt with additional audit metadata.
    """
    phone_number: str
    otp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
