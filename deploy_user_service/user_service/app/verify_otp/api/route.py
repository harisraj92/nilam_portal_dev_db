from fastapi import APIRouter, Depends, status, HTTPException,Request  
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.app.common.db import get_db
from user_service.app.verify_otp.schema import VerifyOtpRequest, TokenResponse
from user_service.app.verify_otp.service import process_verify_otp
import logging
router = APIRouter()

logger = logging.getLogger(__name__)

@router.post(
    "/verify-otp",
    response_model=TokenResponse,
    summary="Verify OTP and get JWT",
    status_code=status.HTTP_200_OK  # ✅ explicitly set success status
)
async def verify_otp_handler(
    request: Request,
    payload: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db)
    
):
    try:
         client_ip = request.client.host
         user_agent = request.headers.get("user-agent", "unknown")
         logger.info(f"OTP verification request from {client_ip} using {user_agent}")

         result = await process_verify_otp(payload, db, client_ip, user_agent)
    except Exception as e:
        # 🔴 fallback if any unhandled error occurs
        logger.exception("Unhandled exception during OTP verification")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong during OTP verification"
        )

    if not result.get("success"):
        # 🔁 401 only if OTP is wrong/expired
        logger.info(f"OTP verification failed for {payload.phone_number}: {result['message']}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("message", "OTP verification failed")
        )

    # ✅ structured response if success
    return TokenResponse(
        access_token=result["access_token"],
        message=result["message"],
        user=result["user"]
    )
