# user_service/app/verify_otp/service.py

import hashlib
from datetime import datetime
import pytz

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from user_service.app.send_otp.model.otp_attempt import OTPAttempt, OTPStatus
from user_service.app.send_otp.model.otp_audit_log import OTPAuditLog, OTPAction, OTPAuditStatus
from user_service.app.auth_token.token_handler import create_access_token
from user_service.app.verify_otp.helper import is_otp_expired, has_exceeded_attempts
from user_service.app.user.model import User  # Optional: for user lookup


# ✅ Hash OTP
def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

# ✅ Get naive UTC
def get_naive_utc_now() -> datetime:
    return datetime.now(pytz.utc).replace(tzinfo=None)


# ✅ Helper: Fetch OTPAttempt with expiry check
async def get_valid_otp_attempt(phone_number: str, db: AsyncSession) -> OTPAttempt | None:
    result = await db.execute(
        select(OTPAttempt)
        .where(
            OTPAttempt.phone_number == phone_number,
            OTPAttempt.status == OTPStatus.pending
        )
        .order_by(OTPAttempt.created_at.desc())
        .limit(1)
    )
    otp_attempt = result.scalar_one_or_none()

    if otp_attempt and is_otp_expired(otp_attempt.expires_at):
        await db.execute(
            update(OTPAttempt)
            .where(OTPAttempt.id == otp_attempt.id)
            .values(status=OTPStatus.expired)
        )
        await db.commit()
        return None  # expired, so return None

    return otp_attempt



# ✅ Main verify OTP logic
async def process_verify_otp(payload, db: AsyncSession, ip_address: str = None, user_agent: str = None) -> dict:

    now = get_naive_utc_now()

    # Step 1: Get latest OTPAttempt
    otp_attempt = await get_valid_otp_attempt(payload.phone_number, db)

    if not otp_attempt:
        db.add(OTPAuditLog(
            phone_number=payload.phone_number,
            action=OTPAction.verify,
            status=OTPAuditStatus.failed,
            timestamp=now,
            ip_address=ip_address,
            user_agent=user_agent
        ))
        await db.commit()
        return {
            "success": False,
            "message": "OTP not found or already used",
            "access_token": None
        }

    # Step 2: Check if too many attempts
    if has_exceeded_attempts(otp_attempt.attempts):
        await db.execute(
            update(OTPAttempt)
            .where(OTPAttempt.id == otp_attempt.id)
            .values(status=OTPStatus.expired)
        )
        db.add(OTPAuditLog(
            phone_number=payload.phone_number,
            action=OTPAction.verify,
            status=OTPAuditStatus.rate_limited,
            timestamp=now
        ))
        await db.commit()
        return {
            "success": False,
            "message": "Too many failed attempts. Please request a new OTP.",
            "access_token": None
        }

    # Step 3: Expired OTP
    if is_otp_expired(otp_attempt.expires_at):
        await db.execute(
            update(OTPAttempt)
            .where(OTPAttempt.id == otp_attempt.id)
            .values(status=OTPStatus.expired)
        )
        db.add(OTPAuditLog(
            phone_number=payload.phone_number,
            action=OTPAction.verify,
            status=OTPAuditStatus.failed,
            timestamp=now,
            ip_address=ip_address,
            user_agent=user_agent
        ))
        await db.commit()
        return {
            "success": False,
            "message": "OTP has expired. Please request a new one.",
            "access_token": None
        }

    # Step 4: Incorrect OTP
    if otp_attempt.otp_hash != hash_otp(payload.otp):
        await db.execute(
            update(OTPAttempt)
            .where(OTPAttempt.id == otp_attempt.id)
            .values(attempts=otp_attempt.attempts + 1)
        )
        db.add(OTPAuditLog(
            phone_number=payload.phone_number,
            action=OTPAction.verify,
            status=OTPAuditStatus.failed,
            timestamp=now,
            ip_address=ip_address,
            user_agent=user_agent
        ))
        await db.commit()
        return {
            "success": False,
            "message": "Incorrect OTP. Please try again.",
            "access_token": None
        }

    # Step 5: Valid OTP – mark verified
    await db.execute(
        update(OTPAttempt)
        .where(OTPAttempt.id == otp_attempt.id)
        .values(status=OTPStatus.verified, attempts=0)
    )
    db.add(OTPAuditLog(
        phone_number=payload.phone_number,
        action=OTPAction.verify,
        status=OTPAuditStatus.success,
        timestamp=now,
        ip_address=ip_address,
        user_agent=user_agent
    ))
    await db.commit()

    # Step 6: Generate token
    token_data = {
        "sub": otp_attempt.phone_number,
        "phone_number": otp_attempt.phone_number,
        "auth": "otp"
    }
    access_token = create_access_token(data=token_data)

    # Step 7: Fetch user info (MUST exist)
    user_result = await db.execute(
        select(User).where(User.phone_number == payload.phone_number)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        return {
            "success": False,
            "message": "User account not found for this OTP.",
            "access_token": None
        }

    user_data = {
        "id": user.id,
        "fullname": user.fullname,
        "phone_number": user.phone_number
    }

    return {
        "success": True,
        "message": "OTP verified successfully",
        "access_token": access_token,
        "user": user_data
    }

