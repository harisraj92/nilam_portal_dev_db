from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import AsyncSessionLocal
from app.services.auth.otp import send_otp_to_user
from app.services.common.utils import normalize_contact

router = APIRouter()
print("[DEBUG] send_otp.py: router initialized")


# Define request body model
class OTPRequest(BaseModel):
    contact: str


# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# ✅ OPTIONS handler for CORS preflight
@router.options("/send-otp")
async def preflight_handler():
    print("[DEBUG] Preflight CORS handled")
    return Response(status_code=200)


# ✅ Main handler to send OTP
@router.post("/send-otp")
async def request_otp(
    payload: OTPRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    try:
        normalized = normalize_contact(payload.contact)
        print(f"[SEND OTP] Contact: {normalized}")

        otp = await send_otp_to_user(db, normalized, background_tasks)
        print(f"[OTP GENERATED] {otp}")
        print("[TASK] Triggered SMS background")

        return {"success": True, "message": "OTP sent successfully"}

    except HTTPException as e:
        print(f"[ERROR] HTTPException: {e.detail}")
        raise e

    except Exception as e:
        print(f"[ERROR] Unexpected: {e}")
        raise HTTPException(status_code=500, detail="Internal error")
