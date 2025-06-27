from sqlalchemy import select
from app.db.models import CustomerProperty
from app.schemas.header.property_dropdown import PropertyDropdownOut

async def get_property_dropdown_by_user(user_id: str, db):
    result = await db.execute(
        select(CustomerProperty).where(CustomerProperty.user_id == user_id)
    )
    records = result.scalars().all()
    return [PropertyDropdownOut.model_validate(r) for r in records]
