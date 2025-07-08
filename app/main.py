from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.authentication import routes as auth_routes
from app.api.sidebar import routes as sidebar_routes
from app.api.header.properties.routes import router as property_router
from app.api.customer.dashboard.property_summary import get_user_properties
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings

app = FastAPI(
    title="Nilam Insights Portal API",
    version="1.0.0",
    description="Secure login with OTP and Twilio integration"
)

print(f"[Startup Check] Loaded SECRET_KEY = {settings.SECRET_KEY}")


origins = [
    "http://localhost:3000",        # Vercel or local frontend  
]


# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🟢 FRONTEND_ORIGIN from settings:", settings.FRONTEND_ORIGIN)

# DB Table Creation on Startup
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ✅ Include your routers
app.include_router(auth_routes.router)
app.include_router(sidebar_routes.router) 
app.include_router(property_router, prefix="/header/properties", tags=["Properties"])
app.include_router(get_user_properties.router, prefix="/api", tags=["Customer Property Cards"])


# Root health check
@app.get("/")
def root():
    return {"message": "Nilam Insights Portal API is running"}