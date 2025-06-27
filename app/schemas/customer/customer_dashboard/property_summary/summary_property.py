from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PropertySummaryOut(BaseModel):
    id: str
    tenant_id: str
    user_id: str
    property_code: str
    name: str
    plot_number: Optional[str]
    location: str
    landmark: Optional[str]
    area_size: Optional[float]
    measurement_unit: Optional[str]
    type: Optional[str]
    ownership_type: Optional[str]
    purchase_date: Optional[date]
    status: Optional[str]
    verified_status: Optional[str]
    is_active: Optional[bool]
    last_visited_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
