# app\services\header\property_list\property.py


from sqlalchemy import select, cast
from sqlalchemy.dialects.postgresql import UUID
from app.db.models import CustomerProperty
from sqlalchemy.ext.asyncio import AsyncSession

async def get_property_dropdown_by_user(user_id: str, db: AsyncSession):
    result = await db.execute(
        select(
            CustomerProperty.property_code,
            CustomerProperty.name
        )
        .where(CustomerProperty.user_id == cast(user_id, UUID))
        .where(CustomerProperty.is_active == True)
    )
    rows = result.all()
    return [dict(row._mapping) for row in rows]

