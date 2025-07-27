import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from user_service.app.config import settings

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

# Declare Base for model usage
Base = declarative_base()

# Create async engine
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    #echo=(settings.env == "dev"),
    echo=False,
    future=True
)

# Session factory
AsyncSessionLocal: sessionmaker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        logger.exception("❌ Database session error")
        raise e
