from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from user_service.app.common.db import get_db
from user_service.app.rbac.model import UserPagePermission
from user_service.app.rbac.schema import PermissionItem
from user_service.app.rbac.service import get_permissions_by_role

router = APIRouter(
    prefix="/rbac",
    tags=["RBAC"]
)

@router.get("/permissions/{role}", response_model=List[PermissionItem])
async def get_permissions(role: str, db: AsyncSession = Depends(get_db)):
    return await get_permissions_by_role(role, db)
