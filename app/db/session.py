# app/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import AsyncGenerator
from app.core.config import settings

# Create async engine using the correct field from settings


engine = create_async_engine(
    settings.database_url,  # ✅ Use lowercase 'database_url' as defined in config.py
    echo=True,
    connect_args={"ssl": "require"}  # ✅ Required for Azure PostgreSQL
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# ✅ Provide dependency to inject DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
     async with AsyncSessionLocal() as session:
        yield session