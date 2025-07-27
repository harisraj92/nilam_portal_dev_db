# user_service/app/send_otp/service.py

import hashlib
import secrets
from datetime import datetime, timedelta
import pytz  # ✅ Added for proper UTC handling

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from user_service.app.send_otp.model.otp_attempt import OTPAttempt, OTPStatus
from user_service.app.send_otp.model.otp_audit_log import OTPAuditLog, OTPAction, OTPAuditStatus
from user_service.app.send_otp.sms_gateway import send_sms
from user_service.app.user.model import User
from user_service.app.config import settings
from user_service.app.common.constants import (
    MSG_OTP_SENT,
    MSG_TOO_MANY_REQUESTS,
    MSG_USER_NOT_FOUND,
)


# ✅ Generate secure numeric OTP
def generate_otp(length: int = 6) -> str:
    return ''.join(secrets.choice("0123456789") for _ in range(length))


# ✅ Hash OTP securely using SHA-256
def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()


# ✅ Correct UTC time helper (naive UTC datetime)
def get_naive_utc_now() -> datetime:
    return datetime.now(pytz.utc).replace(tzinfo=None)  # ✅ FIXED


# ✅ Main function to process OTP generation and sending
async def process_send_otp(phone_number: str, db: AsyncSession, ip_address: str = None, user_agent: str = None) -> dict:

    now = get_naive_utc_now()

    # Step 1: Check if user exists
    user_result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        return {"success": False, "message": MSG_USER_NOT_FOUND}

    # Step 2: Generate OTP
    otp = generate_otp(settings.otp_length)
    otp_hash = hash_otp(otp)
    expires_at = now + timedelta(seconds=settings.otp_expiry_seconds)

    # Step 3: Check for recent OTP
    result = await db.execute(
        select(OTPAttempt)
        .where(OTPAttempt.phone_number == phone_number)
        .order_by(OTPAttempt.created_at.desc())
        .limit(1)
    )
    existing = result.scalar_one_or_none()

    if existing and existing.status == OTPStatus.pending and existing.expires_at > now:
        retry_secs = int((existing.expires_at - now).total_seconds())

        audit_log = OTPAuditLog(
            phone_number=phone_number,
            action=OTPAction.send,
            status=OTPAuditStatus.rate_limited,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=now
        )
        db.add(audit_log)
        await db.commit()

        return {
            "success": False,
            "message": MSG_TOO_MANY_REQUESTS,
            "retry_after_seconds": retry_secs,
        }

    # Step 4: Create/Update OTPAttempt
    if existing:
        existing.otp_hash = otp_hash
        existing.expires_at = expires_at
        existing.last_sent_at = now
        existing.status = OTPStatus.pending
        existing.attempts = 0
        db.add(existing)
    else:
        new_attempt = OTPAttempt(
            phone_number=phone_number,
            otp_hash=otp_hash,
            expires_at=expires_at,
            last_sent_at=now,
            created_at=now,
        )
        db.add(new_attempt)

    # Step 5: Send OTP via SMS
    message = f"Your OTP is {otp}"
    try:
        sms_sent = await send_sms(phone_number, message)
    except Exception:
        sms_sent = False

    # Step 6: Log audit
    audit_log = OTPAuditLog(
        phone_number=phone_number,
        action=OTPAction.send,
        status=OTPAuditStatus.success if sms_sent else OTPAuditStatus.failed,
        ip_address=None,
        user_agent=None,
        timestamp=now
    )
    db.add(audit_log)

    # Step 7: Commit to DB
    await db.commit()

    return {
        "success": sms_sent,
        "message": MSG_OTP_SENT if sms_sent else "Failed to send OTP. Please try again.",
    }
