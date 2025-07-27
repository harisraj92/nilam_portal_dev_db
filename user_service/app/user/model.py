# user_service/app/user/model.py

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from user_service.app.common.db import Base  # this should point to declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "user_service"}  

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, default="customer")
    fullname = Column(String, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
