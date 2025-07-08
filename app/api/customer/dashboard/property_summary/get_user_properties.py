from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.deps import get_db
from app.core.auth import get_current_user
from app.schemas.customer.customer_dashboard.property_summary.summary_property import PropertyCardOut
from app.services.customer.dashboard.property_summary.property_summary_overview import fetch_property_cards


router = APIRouter()

@router.get("/customer/properties/summary", response_model=list[PropertyCardOut])
async def get_property_summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_uuid: UUID = UUID(current_user.id) if isinstance(current_user.id, str) else current_user.id
    return await fetch_property_cards(user_uuid, db)
