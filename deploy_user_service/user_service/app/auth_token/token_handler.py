# user_service/app/auth_token/token_handler.py
from jose import jwt, JWTError
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import os

# You can import SECRET_KEY and ALGORITHM from your config or .env
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_in_prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour by default

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT token for the given data dictionary.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodes and validates the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
