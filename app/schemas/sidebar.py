from pydantic import BaseModel
from typing import List, Optional

class SubMenuItem(BaseModel):
    label: str
    iconClass: Optional[str] = ""

class SidebarItem(BaseModel):
    label: str
    iconClass: Optional[str] = ""
    submenu: List[SubMenuItem] = []
