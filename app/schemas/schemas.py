from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.enums import OTPStatusEnum  # Make sure to import your Enum

# --- Public API Schemas ---

class OTPRequest(BaseModel):
    """
    Schema to request an OTP (phone number/email).
    """
    phone_number: str = Field(..., example="+917010001599")


class OTPVerify(BaseModel):
    """
    Schema to verify an OTP.
    """
    phone_number: str = Field(..., example="+917010001599")
    otp: str = Field(..., example="123456")


class OTPResponse(BaseModel):
    """
    Response schema after sending/verifying OTP.
    """
    success: bool
    message: str


# --- Internal Schemas ---

class OTPAttemptCreate(BaseModel):
    """
    Schema for creating/updating an OTP attempt record in DB.
    """
    phone_number: str
    otp_hash: str
    expires_at: datetime
    last_sent_at: datetime
    status: OTPStatusEnum = OTPStatusEnum.pending


class OTPVerifyAttempt(BaseModel):
    """
    Schema to verify an OTP with audit info.
    """
    phone_number: str
    otp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
