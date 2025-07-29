from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from properties_service.app.schema.user import User
from properties_service.app.config.settings import settings
from jose import jwt, JWTError

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        print("Decoded JWT payload:", payload)

        user_id = payload.get("sub")
        fullname = payload.get("fullname")
        email = payload.get("email")                # ✅ required
        role = payload.get("role")                  # ✅ required
        phone_number = payload.get("phone_number")  # ✅ if schema has this

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return User(
            id=user_id,
            fullname=fullname,
            email=email,
            role=role,
            phone_number=phone_number
        )

    except JWTError as e:
        print("JWT decode error:", e)
        raise HTTPException(status_code=401, detail="Could not validate token")
