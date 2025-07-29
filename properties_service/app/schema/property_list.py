# properties_service/app/schema/property_list.py
from pydantic import BaseModel
from uuid import UUID

class PropertyNameResponse(BaseModel):
    id: UUID
    property_code: str
    name: str
