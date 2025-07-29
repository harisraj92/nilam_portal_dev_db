from sqlalchemy import Column, String, Text, Float, Boolean, Date, DateTime, ForeignKey, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum
import uuid

Base = declarative_base()



class MeasurementUnitEnum(str, PyEnum):
    square_feet = "square_feet"
    cent = "cent"
    acre = "acre"
    hectare = "hectare"

class PropertyTypeEnum(str, PyEnum):
    residential = "residential"
    commercial = "commercial"
    industrial = "industrial"
    agricultural = "agricultural"

class OwnershipTypeEnum(str, PyEnum):
    selfOwned = "selfOwned"
    inherited = "inherited"
    gifted = "gifted"
    leased = "leased"

class VerifiedStatusEnum(str, PyEnum):
    pending = "pending"
    verified = "verified"

class RiskLevelEnum(str, PyEnum):
    high = "high"
    moderate = "moderate"
    low = "low"

class FenceStatusEnum(str, PyEnum):
    fenced = "fenced"
    unfenced = "unfenced"



class CustomerProperty(Base):
    __tablename__ = "customer_properties"
    __table_args__ = {"schema": "properties"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    property_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    location = Column(Text)
    landmark = Column(Text)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    area_size = Column(Float)

    measurement_unit = Column(Enum(
        MeasurementUnitEnum,
        name="measurement_unit",
        native_enum=False,
        create_type=False,
        schema="properties"
    ))

    type = Column(Enum(
        PropertyTypeEnum,
        name="property_type",
        native_enum=False,
        create_type=False,
        schema="properties"
    ))

    plot_type = Column(Enum(
        PropertyTypeEnum,
        name="property_type",
        native_enum=False,
        create_type=False,
        schema="properties"
    ))

    ownership_type = Column(Enum(
        OwnershipTypeEnum,
        name="ownership_type",
        native_enum=False,
        create_type=False,
        schema="properties"
    ))

    purchase_date = Column(Date)
    market_value = Column(Float)
    ownership_proof_url = Column(Text)
    description = Column(Text)
    status = Column(Boolean, default=True)

    verified_status = Column(Enum(
        VerifiedStatusEnum,
        name="verified_status",
        native_enum=False,
        create_type=False,
        schema="properties"
    ), default=VerifiedStatusEnum.pending)

    risk_level = Column(Enum(
        RiskLevelEnum,
        name="risk_level",
        native_enum=False,
        create_type=False,
        schema="properties"
    ))

    fence_status = Column(Enum(
        FenceStatusEnum,
        name="fence_status",
        native_enum=False,
        create_type=False,
        schema="properties"
    ))

    is_active = Column(Boolean, default=True)
    last_visited_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
    remarks = Column(Text)
    visit_plan = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    photo_url = Column(Text, nullable=True)
