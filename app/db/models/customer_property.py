#app\db\models\customer_property.py
from sqlalchemy import (
    Column, String, Boolean, Date, DateTime, Text, Numeric, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid
from datetime import datetime


class CustomerProperty(Base):
    __tablename__ = "customer_properties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    property_code = Column(String(50), unique=True, nullable=False)
    name = Column(String, nullable=False)
    plot_number = Column(String)
    location = Column(Text, nullable=False)
    landmark = Column(Text)

    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    area_size = Column(Numeric(10, 2))
    measurement_unit = Column(String(10))

    type = Column(String)
    plot_type = Column(String(50))
    ownership_type = Column(String)
    purchase_date = Column(Date)
    market_value = Column(Numeric(14, 2))

    ownership_proof_url = Column(Text)
    description = Column(Text)
    status = Column(String)
    verified_status = Column(String(20), default="pending")
    risk_level = Column(String(20))
    is_active = Column(Boolean, default=True)

    last_visited_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True))
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(UUID(as_uuid=True))

    remarks = Column(Text)
    fence_status =  Column(String(20))
