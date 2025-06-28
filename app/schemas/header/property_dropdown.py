from pydantic import BaseModel

class PropertyDropdownOut(BaseModel):
    id: str
    label: str   # ✅ இது முக்கியம்

    class Config:
        from_attributes = True
