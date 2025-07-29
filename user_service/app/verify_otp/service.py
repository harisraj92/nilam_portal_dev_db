import hashlib
from datetime import datetime
import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from user_service.app.send_otp.model.otp_attempt import OTPAttempt, OTPStatus
from user_service.app.send_otp.model.otp_audit_log import OTPAuditLog, OTPAction, OTPAuditStatus
from user_service.app.auth_token.token_handler import create_access_token
from user_service.app.verify_otp.helper import is_otp_expired, has_exceeded_attempts
from user_service.app.user.model import User


def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()


def get_naive_utc_now() -> datetime:
    return datetime.now(pytz.utc).replace(tzinfo=None)


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
        return None

    return otp_attempt


async def process_verify_otp(payload, db: AsyncSession, ip_address: str = None, user_agent: str = None) -> dict:
    now = get_naive_utc_now()

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
        "id": str(user.id),
        "fullname": user.fullname or "User",       
        "role": user.role or "customer",
        "phone_number": user.phone_number
    }

    try:
        access_token = create_access_token(data=user_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": "Something went wrong while creating token",
            "access_token": None
        }

    return {
        "success": True,
        "message": "OTP verified successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }
