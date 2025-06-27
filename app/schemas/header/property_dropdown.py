from pydantic import BaseModel

class PropertyDropdownOut(BaseModel):
    id: str
    name: str
    location: str | None = None

    class Config:
        from_attributes = True  # ✅ for Pydantic v2
