# app/services/utils.py

from datetime import datetime, timedelta, timezone

def normalize_contact(input_value: str) -> str:
    input_value = input_value.strip()
    if "@" in input_value:
        return input_value.lower()
    elif input_value.startswith("+"):
        return input_value
    else:
        return f"+91{input_value}"

def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    if phone.startswith("+91"):
        phone = phone[3:]
    return phone[-10:]

def get_expiry_timestamp(minutes=5):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)

def now_utc():
    return datetime.now(timezone.utc)  # ✅ FIX: timezone-aware
