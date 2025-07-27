# file: user_service/app/send_otp/model/otp_audit_log.py

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from enum import Enum as PyEnum

from user_service.app.common.db import Base

# ✅ Python Enum
class OTPAuditStatus(PyEnum):
    success = "success"
    failed = "failed"
    rate_limited = "rate_limited"


class OTPAction(PyEnum):
    send = "send"
    verify = "verify"

class OTPAuditLog(Base):
    __tablename__ = "otp_audit_log"
    __table_args__ = {"schema": "auth_service"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False)
    
    # ✅ Use SQLEnum and name/schema set correctly
    action = Column(SQLEnum(OTPAction, name="otp_action", schema="auth_service"), nullable=False)
    status = Column(SQLEnum(OTPAuditStatus, name="otp_audit_status", schema="auth_service"), nullable=False)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
