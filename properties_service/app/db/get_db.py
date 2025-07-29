# properties_service/app/db/db.py
from properties_service.app.db.database import async_session

async def get_db():
    async with async_session() as session:
        yield session
