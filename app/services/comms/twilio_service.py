# app/services/twilio_service.py

from twilio.rest import Client
from app.core.config import settings

def send_sms(to: str, body: str):
    try:
        print(f"[Twilio] Sending to {to}: {body}")
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        print(f"[Twilio] SID: {message.sid}, Status: {message.status}")
    except Exception as e:
        print(f"[Twilio Error] Failed to send SMS: {e}")
        raise

def trigger_sms_background(phone_number: str, otp: str):
    try:
        send_sms(to=phone_number, body=f"Your OTP is: {otp}")
        print(f"[INFO] OTP sent in background to {phone_number}")
    except Exception as e:
        print(f"[ERROR] Background SMS failed: {e}")
