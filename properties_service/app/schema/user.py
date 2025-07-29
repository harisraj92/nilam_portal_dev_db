# properties_service/app/schema/user.py

from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    id: UUID
    fullname: str
    role: str
    phone_number: str
