from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.db.models import PagePermission
from app.schemas.sidebar.sidebar_item import SidebarItem, SubmenuItem

router = APIRouter(
    prefix="/sidebar",
    tags=["Sidebar"]
)

@router.get("/{role}", response_model=List[SidebarItem])
async def get_sidebar(role: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PagePermission)
        .where(PagePermission.role == role)
        .order_by(PagePermission.order)
    )
    permissions = result.scalars().all()

    parent_labels = {
        item.parent_label for item in permissions
        if item.is_submenu and item.parent_label
    }

    sidebar = {}

    for item in permissions:
        if item.label in parent_labels:
            sidebar.setdefault(item.label, {
                "label": item.label,
                "iconClass": item.icon_class or "",
                "submenu": []
            })

        if item.is_submenu and item.parent_label:
            sidebar.setdefault(item.parent_label, {
                "label": item.parent_label,
                "iconClass": "",
                "submenu": []
            })

            sidebar[item.parent_label]["submenu"].append({
                "label": item.label,
                "iconClass": item.icon_class or "",
                "href": item.href or ""
            })

        elif item.label not in parent_labels:
            sidebar[item.label] = {
                "label": item.label,
                "iconClass": item.icon_class or "",
                "href": item.href or "",
                "submenu": []
            }

    # Final: Convert to SidebarItem Pydantic models
    return [SidebarItem(**item) for item in sidebar.values()]
