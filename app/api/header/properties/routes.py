from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.services.property.property_service import get_property_dropdown_by_user
from app.schemas.header.property_dropdown import PropertyDropdownOut
from app.core.auth import get_current_user
import logging

logger = logging.getLogger("properties")

router = APIRouter()

@router.get("/property-dropdown", response_model=list[PropertyDropdownOut])
async def fetch_property_dropdown(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info("✅ property-dropdown endpoint hit")
    return await get_property_dropdown_by_user(current_user.id, db)
