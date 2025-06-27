from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import AsyncSessionLocal
from app.services.auth.otp import verify_otp_and_login
from app.services.common.utils import normalize_contact


router = APIRouter()

# ✅ Request schema for JSON body
class OTPVerifyRequest(BaseModel):
    contact: str
    otp: str

# ✅ DB dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# ✅ Route to verify OTP
@router.post("/verify-otp")
async def verify_otp(
    payload: OTPVerifyRequest,
    db: AsyncSession = Depends(get_db)
):
    normalized = normalize_contact(payload.contact)
    print(f"[VERIFY OTP] Attempt for: {normalized}")

    try:
        token = await verify_otp_and_login(db, normalized, payload.otp)
        return {
            "success": True,
            "message": "OTP verified successfully",
            "access_token": token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        print(f"[ERROR] HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
