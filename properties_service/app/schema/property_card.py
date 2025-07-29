from pydantic import BaseModel
from pydantic import HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime

class PropertyCard(BaseModel):
    property_id: UUID
    property_name: Optional[str]
    property_code: Optional[str]  # ✅ ADD THIS
    property_code_name: Optional[str]
    location: Optional[str]
    last_visited: Optional[datetime]
    fencing_status: Optional[str]
    risk_level: Optional[str]
    alert_count: Optional[int]
    remarks: Optional[str]
    photo_url: Optional[HttpUrl]

    class Config:
        orm_mode = True
