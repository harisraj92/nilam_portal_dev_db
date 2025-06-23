from fastapi import APIRouter, Depends
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/protected-endpoint")
async def protected(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": current_user
    }
