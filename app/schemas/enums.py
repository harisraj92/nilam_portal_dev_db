from enum import Enum

class OTPStatusEnum(str, Enum):
    """
    Enum representing the status of an OTP attempt.
    """
    pending = "pending"
    verified = "verified"
    expired = "expired"
