from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from properties_service.app.db.database import settings
from properties_service.app.route.property_route import router as property_router
from properties_service.app.route.property_summary import router as summary_router

app = FastAPI(
    title="Nilam Portal Property Service",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",  # adjust if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(property_router)
app.include_router(summary_router)

@app.get("/")
async def root():
    return {"message": "Property Service Running", "env": settings.env}
