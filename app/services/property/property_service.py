# app/services/property/property_service.py
from sqlalchemy import select, cast
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from app.db.models import CustomerProperty
from sqlalchemy.ext.asyncio import AsyncSession

async def get_property_dropdown_by_user(user_id: str, db: AsyncSession):
    result = await db.execute(
        select(CustomerProperty)
        .where(CustomerProperty.user_id == cast(user_id, UUID))
        .where(CustomerProperty.is_active == True)
    )
    properties = result.scalars().all()
    return [
        {
            "id": str(prop.id),  # ✅ Fix here
            "label": f"{prop.plot_number or ''} – {prop.location or prop.name}"
        }
        for prop in properties
    ]
