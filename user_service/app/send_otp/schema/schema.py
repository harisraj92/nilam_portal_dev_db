# user_service/app/features/send_otp/schema.py

from pydantic import BaseModel, Field
from typing import Optional

# 👉 Incoming request body for /send-otp
class SendOtpRequest(BaseModel):
    phone_number: str = Field(..., example="+919876543210")

# 👉 Outgoing response for successful OTP generation
class SendOtpResponse(BaseModel):
    success: bool = True
    message: str = "OTP sent successfully"

# 👉 Optional: Response when OTP already sent recently
class OtpAlreadySentResponse(BaseModel):
    success: bool = False
    message: str = "OTP already sent. Please wait before retrying."
    retry_after_seconds: Optional[int] = None
