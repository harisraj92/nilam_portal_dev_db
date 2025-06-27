from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base

class CustomerProperty(Base):
    __tablename__ = "customer_properties"

    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    property_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    plot_number = Column(String, nullable=True)
    location = Column(String, nullable=True)
    landmark = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    area_size = Column(String, nullable=True)
    measurement_unit = Column(String, nullable=True)
    type = Column(String, nullable=True)
    plot_type = Column(String, nullable=True)
    ownership_type = Column(String, nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    market_value = Column(String, nullable=True)
    ownership_proof_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(String, nullable=True)
    verified_status = Column(String, nullable=True)
    risk_level = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_visited_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    created_by = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String, nullable=True)
