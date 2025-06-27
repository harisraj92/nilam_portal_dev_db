from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, ENUM as PgEnum
from sqlalchemy.sql import func
import uuid

from app.schemas.enums import OTPStatusEnum
from app.db.base import Base

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
