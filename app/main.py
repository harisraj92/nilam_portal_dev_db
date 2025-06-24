from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.authentication import routes as auth_routes
from app.api.sidebar import routes as sidebar_routes
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="Nilam OTP Auth API",
    version="1.0.0",
    description="Secure login with OTP and Twilio integration"
)


# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Table Creation on Startup
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ✅ Include your routers
app.include_router(auth_routes.router)
app.include_router(sidebar_routes.router) 


# Root health check
@app.get("/")
def root():
    return {"message": "Nilam OTP API is running"}