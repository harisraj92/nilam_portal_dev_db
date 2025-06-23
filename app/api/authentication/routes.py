from fastapi import APIRouter
from app.api.authentication import send_otp, verify_otp, protected

# Define the main router for all authentication-related routes
router = APIRouter()

# Group all authentication-related routes under the "/auth" prefix
router.include_router(send_otp.router, prefix="/auth", tags=["Auth"])
router.include_router(verify_otp.router, prefix="/auth", tags=["Auth"])
router.include_router(protected.router, prefix="/auth", tags=["Auth"])
