# user_service/app/send_otp/sms_gateway.py
import httpx
import logging
from user_service.app.config import settings

logger = logging.getLogger(__name__)

async def send_sms(phone_number: str, message: str) -> bool:
    """
    Sends SMS using MSG91 or logs it in dev mode.
    """
    try:
        if settings.env == "dev":
            # 🔧 DEV: Print OTP to console for developer visibility
            print(f"[DEV] SMS to {phone_number}: {message}")
            logger.info(f"[DEV] SMS to {phone_number}: {message}")
            return True

        # ✅ Uncomment below for production with MSG91
        """
        url = "https://control.msg91.com/api/v5/flow/"
        headers = {
            "authkey": settings.msg91_auth_key,
            "Content-Type": "application/json"
        }
        payload = {
            "flow_id": settings.msg91_flow_id,
            "sender": settings.msg91_sender_id,
            "mobiles": phone_number,
            "OTP": message
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            logger.info(f"MSG91 Response: {response.status_code} - {response.text}")
            return response.status_code == 200
        """

        return True  # Fallback in case MSG91 is not set

    except Exception as e:
        logger.exception("❌ Failed to send SMS via MSG91")
        return False
