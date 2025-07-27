import random
import string
from datetime import datetime, timedelta, timezone
import pytz

# ✅ Generate random OTP (numbers only)
def generate_numeric_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

# ✅ Check if OTP is expired (uses timezone-aware UTC)
def is_otp_expired(created_time: datetime, expiry_seconds: int = 300) -> bool:
    """
    Returns True if the OTP has expired.
    created_time must be timezone-aware.
    """
    now = datetime.now(timezone.utc)
    return now > (created_time + timedelta(seconds=expiry_seconds))

# ✅ Mask mobile number for logging
def mask_mobile(mobile: str) -> str:
    if len(mobile) < 5:
        return '*' * len(mobile)
    return mobile[:3] + '*' * (len(mobile) - 5) + mobile[-2:]

# ✅ Get timezone-aware current UTC datetime
def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# ✅ Convert UTC datetime to IST (for display/logging only)
def convert_utc_to_ist(utc_dt: datetime) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    return utc_dt.astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
