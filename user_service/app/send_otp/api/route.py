# user_service/app/send_otp/api/router.py
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from user_service.app.send_otp.schema.schema import SendOtpRequest, SendOtpResponse, OtpAlreadySentResponse
from user_service.app.send_otp.service import process_send_otp
from user_service.app.common.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post(
    "/send-otp",
    response_model=SendOtpResponse,
    responses={429: {"model": OtpAlreadySentResponse}},
    summary="Send OTP to phone number",
)
async def send_otp_handler(
    request: Request,
    payload: SendOtpRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    👉 Receives a phone number and sends OTP  
    ✅ Rate-limited, audit-logged, OTP stored in DB
    """

    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    result = await process_send_otp(payload.phone_number, db,client_ip, user_agent)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

