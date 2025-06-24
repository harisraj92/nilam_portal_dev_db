from sqlalchemy import Column, String, Boolean, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import UUID, ENUM as PgEnum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
import uuid

from app.schemas.enums import OTPStatusEnum
from app.db.base import Base

# ----------------------------
# User Table
# ----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="customer")
    tenant_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ----------------------------
# Local Enums for Audit Log
# ----------------------------
class OTPAction(PyEnum):
    send = "send"
    verify = "verify"


class OTPAuditStatus(PyEnum):
    success = "success"
    failed = "failed"
    rate_limited = "rate_limited"


# ----------------------------
# OTP Attempts Table
# ----------------------------
class OTPAttempt(Base):
    __tablename__ = "otp_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False)
    otp_hash = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    attempts = Column(Integer, default=0)
    last_sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(
        PgEnum(OTPStatusEnum, name="otp_status", create_type=False),
        nullable=False,
        default=OTPStatusEnum.pending
    )


# ----------------------------
# OTP Audit Log Table
# ----------------------------
class OTPAuditLog(Base):
    __tablename__ = "otp_audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False)
    action = Column(
        PgEnum(OTPAction, name="otp_action", create_type=False),
        nullable=False
    )
    status = Column(
        PgEnum(OTPAuditStatus, name="otp_result_status", create_type=False),
        nullable=False
    )
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


    # ----------------------------
# Page Permission Table
# ----------------------------
class PagePermission(Base):
    __tablename__ = "user_page_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    role = Column(String, nullable=False)
    label = Column(String, nullable=False)
    is_submenu = Column(Boolean, default=False)
    parent_label = Column(String, nullable=True)
    order = Column(Integer)
    icon_class = Column(String, nullable=True)
    href = Column(String, nullable=True)  # ✅ new column added