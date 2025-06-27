from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM as PgEnum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
import uuid

from app.db.base import Base

class OTPAction(PyEnum):
    send = "send"
    verify = "verify"

class OTPAuditStatus(PyEnum):
    success = "success"
    failed = "failed"
    rate_limited = "rate_limited"

class OTPAuditLog(Base):
    __tablename__ = "otp_audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False)
    action = Column(PgEnum(OTPAction, name="otp_action", create_type=False), nullable=False)
    status = Column(PgEnum(OTPAuditStatus, name="otp_result_status", create_type=False), nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
