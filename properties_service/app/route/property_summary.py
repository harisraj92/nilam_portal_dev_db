from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from properties_service.app.dependencies.auth import get_current_user
from properties_service.app.db.get_db import get_db
from properties_service.app.service.property_service import get_user_property_summary
from properties_service.app.schema.property_card import PropertyCard
from properties_service.app.schema.user import User
from typing import List

router = APIRouter()

@router.get("/api/customer/properties/summary", response_model=List[PropertyCard])
async def get_property_summary(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_user_property_summary(current_user.id, db)
