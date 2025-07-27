from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from user_service.app.rbac.model import UserPagePermission
from user_service.app.rbac.schema import PermissionItem, SubPermissionItem

async def get_permissions_by_role(role: str, db: AsyncSession) -> list[PermissionItem]:
    result = await db.execute(
        select(UserPagePermission)  # ✅ Fixed: use correct model name
        .where(UserPagePermission.role == role)
        .order_by(UserPagePermission.order)
    )
    records = result.scalars().all()

    menu_dict = {}

    for row in records:
        if not row.is_submenu:
            menu_dict[row.label] = {
                "label": row.label,
                "iconClass": row.icon_class or "",
                "href": row.href or "",
                "submenu": [],
            }

    for row in records:
        if row.is_submenu and row.parent_label in menu_dict:
            menu_dict[row.parent_label]["submenu"].append({
                "label": row.label,
                "iconClass": row.icon_class or "",
                "href": row.href or "",
            })

    return [PermissionItem(**item) for item in menu_dict.values()]
