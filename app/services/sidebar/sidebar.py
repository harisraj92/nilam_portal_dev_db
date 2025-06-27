from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import UserPagePermission
from app.schemas.sidebar import SidebarItem, SubMenuItem

async def get_sidebar_by_role(role: str, db: AsyncSession) -> list[SidebarItem]:
    result = await db.execute(
        select(UserPagePermission)
        .where(UserPagePermission.role == role)
        .order_by(UserPagePermission.order)
    )
    records = result.scalars().all()

    menu_dict = {}

    for row in records:
        if not row.is_submenu:
            menu_dict[row.label] = {
                "label": row.label,
                "iconClass": row.icon_class,
                "submenu": [],
            }

    for row in records:
        if row.is_submenu and row.parent_label in menu_dict:
            menu_dict[row.parent_label]["submenu"].append({
                "label": row.label,
                "iconClass": row.icon_class,
            })

    return list(menu_dict.values())
