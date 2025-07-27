# user_service/app/send_otp/otp_attempt.py
# This file defines the OTPAttempt model for the user service, which is used to manage OTP
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from enum import Enum as PyEnum

from user_service.app.common.db import Base  # shared declarative base

class OTPStatus(PyEnum):
    pending = "pending"
    verified = "verified"
    expired = "expired"

class OTPAttempt(Base):
    __tablename__ = "otp_attempts"
    __table_args__ = {"schema": "auth_service"}

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)
    otp_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    attempts = Column(Integer, default=0)
    last_sent_at = Column(DateTime, nullable=True)
    status = Column(
        Enum(OTPStatus, name="otp_status", schema="auth_service"),
        default=OTPStatus.pending,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    #updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
