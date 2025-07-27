# user_service/app/verify_otp/helper.py
from datetime import datetime

# How many attempts allowed per OTP
MAX_OTP_ATTEMPTS = 3

def is_otp_expired(expires_at: datetime) -> bool:
    """
    Returns True if the OTP has expired based on the stored expires_at timestamp.
    """
    if not expires_at:
        return True
    return datetime.utcnow() > expires_at

def has_exceeded_attempts(attempts: int) -> bool:
    """
    Returns True if attempts have reached or exceeded the max.
    """
    return (attempts or 0) >= MAX_OTP_ATTEMPTS
