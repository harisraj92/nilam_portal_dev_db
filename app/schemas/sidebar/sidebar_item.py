#app\schemas\sidebar\sidebar_item.py

from typing import List, Optional
from pydantic import BaseModel

class SubmenuItem(BaseModel):
    label: str
    iconClass: Optional[str] = ""
    href: Optional[str] = ""

class SidebarItem(BaseModel):
    label: str
    iconClass: Optional[str] = ""
    href: Optional[str] = ""
    submenu: List[SubmenuItem] = []