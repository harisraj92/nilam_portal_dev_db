# app/core/auth.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import User
from app.core.config import settings
from pydantic import ValidationError

# ✅ Use HTTPBearer for better Swagger UI
oauth2_scheme = HTTPBearer()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except (JWTError, ValidationError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
