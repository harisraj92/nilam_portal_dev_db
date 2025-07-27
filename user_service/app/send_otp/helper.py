# file: user_service/app/send_otp/helper.py
import random
import hashlib


def generate_otp(length: int = 6) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()


def verify_otp_hash(otp: str, hashed_otp: str) -> bool:
    return hash_otp(otp) == hashed_otp
