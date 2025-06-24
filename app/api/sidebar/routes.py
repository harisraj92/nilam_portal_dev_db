from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import PagePermission

router = APIRouter(
    prefix="/sidebar",
    tags=["Sidebar"]
)

@router.get("/{role}")
async def get_sidebar(role: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PagePermission)
        .where(PagePermission.role == role)
        .order_by(PagePermission.order)
    )
    permissions = result.scalars().all()

    # Step 1: Collect all parent labels (from submenu entries)
    parent_labels = {
        item.parent_label for item in permissions
        if item.is_submenu and item.parent_label
    }

    sidebar = {}

    for item in permissions:
        if item.label in parent_labels:
            # It's a parent menu — no href, has submenu
            if item.label not in sidebar:
                sidebar[item.label] = {
                    "label": item.label,
                    "iconClass": item.icon_class or "",
                    "submenu": []
                }

        if item.is_submenu and item.parent_label:
            # Child item — add to submenu of parent
            if item.parent_label not in sidebar:
                sidebar[item.parent_label] = {
                    "label": item.parent_label,
                    "iconClass": "",
                    "submenu": []
                }

            sidebar[item.parent_label]["submenu"].append({
                "label": item.label,
                "iconClass": item.icon_class or "",
                "href": item.href or ""
            })

        elif item.label not in parent_labels:
            # Regular item (not a parent)
            sidebar[item.label] = {
                "label": item.label,
                "iconClass": item.icon_class or "",
                "href": item.href or "",
                "submenu": []
            }

    return list(sidebar.values())
