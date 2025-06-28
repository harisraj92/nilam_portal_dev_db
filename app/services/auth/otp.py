# app/services/otp.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
import bcrypt, random
from datetime import datetime, timedelta
from fastapi import BackgroundTasks
from app.schemas.enums import OTPStatusEnum
from jose import jwt
from app.db.models import User, OTPAttempt, OTPAuditLog, OTPAuditStatus, OTPAction
from app.services.auth.jwt_handler import create_access_token
from app.services.common.utils import get_expiry_timestamp, now_utc
from app.services.comms.twilio_service import trigger_sms_background
from app.core.config import settings
from uuid import uuid4
from datetime import datetime, timezone


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ----------------------------
# OTP Utilities
# ----------------------------
def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    return bcrypt.hashpw(otp.encode(), bcrypt.gensalt()).decode()

def verify_hash(otp: str, hashed: str) -> bool:
    return bcrypt.checkpw(otp.encode(), hashed.encode())

def normalize_phone(phone: str) -> str:
    return phone[-10:]  # Assumes Indian mobile numbers

# ----------------------------
# Audit Logger
# ----------------------------
async def log_otp_audit(
    db: AsyncSession,
    phone_number: str,
    action: OTPAction,
    status: OTPAuditStatus,
    ip_address: str = "127.0.0.1",
    user_agent: str = "FastAPI"
):
    log_entry = OTPAuditLog(
        id=uuid4(),
        phone_number=phone_number,
        action=action.value,
        status=status.value,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(log_entry)
    await db.commit()

# ----------------------------
# Send OTP
# ----------------------------
from fastapi import BackgroundTasks

async def send_otp_to_user(db: AsyncSession, phone_number: str, background_tasks: BackgroundTasks) -> str:
    print(f"[SEND OTP] Contact: {phone_number}")
    normalized = normalize_phone(phone_number)

    result = await db.execute(select(User).filter(User.phone_number == normalized))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    otp = generate_otp()
    otp_hash = hash_otp(otp)
    expires = get_expiry_timestamp()

    result = await db.execute(select(OTPAttempt).filter(OTPAttempt.phone_number == normalized))
    existing = result.scalar_one_or_none()

    if existing:
        existing.otp_hash = otp_hash
        existing.expires_at = expires
        existing.attempts = 0
        existing.last_sent_at = now_utc()
        existing.status = OTPStatusEnum.pending
    else:
        new = OTPAttempt(
            phone_number=normalized,
            otp_hash=otp_hash,
            expires_at=expires,
            attempts=0,
            last_sent_at=now_utc(),
            created_at=now_utc(),
            status=OTPStatusEnum.pending
        )
        db.add(new)

    await db.commit()
    await log_otp_audit(db, normalized, OTPAction.send, OTPAuditStatus.success)

    background_tasks.add_task(trigger_sms_background, phone_number, otp)  # ✅ Safe async trigger
    return otp

# ----------------------------
# Verify OTP
# ----------------------------
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_otp_and_login(db: AsyncSession, phone_number: str, otp: str) -> str:
    normalized = normalize_phone(phone_number)

    result = await db.execute(select(OTPAttempt).filter(OTPAttempt.phone_number == normalized))
    record = result.scalar_one_or_none()

    if not record:
        await log_otp_audit(db, normalized, OTPAction.verify, OTPAuditStatus.failed)
        raise HTTPException(status_code=404, detail="OTP not found")

    expires_at = record.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now_utc():
        await log_otp_audit(db, normalized, OTPAction.verify, OTPAuditStatus.failed)
        raise HTTPException(status_code=400, detail="OTP expired")

    if record.status == OTPStatusEnum.verified:
        await log_otp_audit(db, normalized, OTPAction.verify, OTPAuditStatus.failed)
        raise HTTPException(status_code=400, detail="OTP already used")

    if not verify_hash(otp, record.otp_hash):
        record.attempts += 1
        await db.commit()
        await log_otp_audit(db, normalized, OTPAction.verify, OTPAuditStatus.failed)
        raise HTTPException(status_code=401, detail="Incorrect OTP")

    # OTP is valid
    record.status = OTPStatusEnum.verified
    await db.commit()
    await log_otp_audit(db, normalized, OTPAction.verify, OTPAuditStatus.success)

    result = await db.execute(select(User).where(User.phone_number == normalized))
    user = result.scalar_one_or_none()

    if not user:
        user = User(phone_number=normalized)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    return token,user
