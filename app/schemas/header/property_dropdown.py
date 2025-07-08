# app/schemas/header/property_dropdown.py
from pydantic import BaseModel

class PropertyDropdownOut(BaseModel):
    property_code: str
    name: str

    class Config:
        from_attributes = True
