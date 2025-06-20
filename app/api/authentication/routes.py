# app/api/authentication/routes.py
from fastapi import APIRouter
from app.api.authentication import send_otp, verify_otp

router = APIRouter()
router.include_router(send_otp.router, prefix="/auth", tags=["Auth"])
router.include_router(verify_otp.router, prefix="/auth", tags=["Auth"])
