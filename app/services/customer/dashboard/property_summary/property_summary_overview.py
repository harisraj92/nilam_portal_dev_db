#app\services\customer\dashboard\property_summary\property_summary_overview.py


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.models.customer_property import CustomerProperty
from app.schemas.customer.customer_dashboard.property_summary.summary_property import PropertyCardOut

async def fetch_property_cards(user_id: UUID, db: AsyncSession) -> list[PropertyCardOut]:
    result = await db.execute(
        select(
            CustomerProperty.id,
            CustomerProperty.name,
            CustomerProperty.property_code,
            CustomerProperty.last_visited_at,
            CustomerProperty.fence_status,
            CustomerProperty.risk_level,
            CustomerProperty.description.label("remarks")
        ).where(CustomerProperty.user_id == str(user_id))
    )
    rows = result.all()
    return [PropertyCardOut(**dict(row._mapping)) for row in rows]
