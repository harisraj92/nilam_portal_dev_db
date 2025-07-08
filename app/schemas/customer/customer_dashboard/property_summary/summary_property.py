#app\schemas\customer\customer_dashboard\property_summary\summary_property.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class PropertyCardOut(BaseModel):
    id: UUID
    name: str
    property_code: str
    last_visited_at: Optional[datetime]
    fence_status: Optional[str]
    risk_level: Optional[str]
    remarks: Optional[str]
