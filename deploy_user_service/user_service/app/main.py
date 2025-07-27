# user_service/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user_service.app.config import settings
from user_service.app.send_otp.api.route import router as send_otp_router
from user_service.app.verify_otp.api.route import router as verify_otp_router
from user_service.app.rbac.route import router as rbac_router

app = FastAPI(
    title="Nilam Portal User Service",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,               
    allow_credentials=True,
    allow_methods=["*"],                 
    allow_headers=["*"],                 
)

app.include_router(send_otp_router, prefix="/auth", tags=["OTP"])
app.include_router(verify_otp_router, prefix="/auth")
app.include_router(rbac_router)

@app.get("/")
async def root():
    return {"message": "User Service Running", "env": settings.env}
