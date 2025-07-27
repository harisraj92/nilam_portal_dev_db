# user_service/app/rbac/schema.py

from typing import List, Optional
from pydantic import BaseModel

class SubPermissionItem(BaseModel):
    label: str
    iconClass: Optional[str] = ""
    href: Optional[str] = ""

class PermissionItem(BaseModel):
    label: str
    iconClass: Optional[str] = ""
    href: Optional[str] = ""
    submenu: List[SubPermissionItem] = []
