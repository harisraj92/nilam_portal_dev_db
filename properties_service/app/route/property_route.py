from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from properties_service.app.service.property_service import get_user_properties
from properties_service.app.schema.property_list import PropertyNameResponse
from properties_service.app.dependencies.auth import get_current_user
from properties_service.app.db.get_db import get_db
from properties_service.app.schema.user import User

router = APIRouter()

@router.get("/header/properties/property-dropdown", response_model=List[PropertyNameResponse])
async def get_property_dropdown(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)  # ✅ db session inject 
):
    return await get_user_properties(current_user.id, db)  # ✅ db argument 
