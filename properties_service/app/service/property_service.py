from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from properties_service.app.model.customer_properties import CustomerProperty
from properties_service.app.schema.property_card import PropertyCard
from properties_service.app.schema.property_list import PropertyNameResponse
from uuid import UUID

# ✅ For /api/customer/properties/summary endpoint
async def get_user_property_summary(user_id: UUID, db: AsyncSession) -> list[PropertyCard]:
    result = await db.execute(
        select(CustomerProperty).where(CustomerProperty.user_id == user_id)  # FIXED HERE
    )
    properties = result.scalars().all()

    return [
        PropertyCard(
            property_id=prop.id,
            property_name=prop.name or "",
            property_code=prop.property_code,
            property_code_name=f"{prop.property_code} - {prop.name or ''}",
            location=prop.location or "",
            last_visited=prop.last_visited_at,
            fencing_status=prop.fence_status.value if prop.fence_status else None,
            risk_level=prop.risk_level.value if prop.risk_level else None,
            alert_count=0,  # You can update based on actual logic later
            remarks=prop.remarks,
            photo_url=prop.photo_url
        )
        for prop in properties
    ]

# ✅ For header dropdown: /header/properties/property-dropdown
async def get_user_properties(user_id: UUID, db: AsyncSession) -> list[PropertyNameResponse]:
    result = await db.execute(
        select(CustomerProperty).where(CustomerProperty.user_id == user_id)  # FIXED HERE
    )
    properties = result.scalars().all()
    return [
    PropertyNameResponse(
        id=prop.id,
        property_code=prop.property_code,
        name=prop.name
    )
    for prop in properties
]
