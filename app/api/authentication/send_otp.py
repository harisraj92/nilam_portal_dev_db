# app/api/authentication/send_otp.py

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import AsyncSessionLocal
from app.services.auth.otp import send_otp_to_user, trigger_sms_background
from app.services.common.utils import normalize_contact

router = APIRouter()

class OTPRequest(BaseModel):
    contact: str

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/send-otp")
async def request_otp(
    payload: OTPRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    try:
        normalized = normalize_contact(payload.contact)
        print(f"[SEND OTP] Contact: {normalized}")

        otp = await send_otp_to_user(db, normalized, background_tasks)  # ✅ Pass background
        print(f"[OTP GENERATED] {otp}")
        print("[TASK] Triggered SMS background")

        return {"success": True, "message": "OTP sent successfully"}

    except HTTPException as e:
        print(f"[ERROR] HTTPException: {e.detail}")
        raise e

    except Exception as e:
        print(f"[ERROR] Unexpected: {e}")
        raise HTTPException(status_code=500, detail="Internal error")

