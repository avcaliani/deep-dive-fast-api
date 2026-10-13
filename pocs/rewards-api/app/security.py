from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException
from jose import JWTError, jwt

from app.config import settings

SECRET_KEY = settings.TOKEN_SECRET_KEY
ALGORITHM = settings.TOKEN_ALGORITHM
EXPIRE_MINUTES = settings.TOKEN_EXPIRE_MINUTES

EXCEPTION_INVALID_CREDENTIALS = HTTPException(
    status_code=401,
    detail="Invalid credentials!",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_token(subject: str, mood: str):
    data = {
        "sub": subject,
        "mood": mood,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES),
    }
    return {"token": jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}


def decode(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as ex:
        raise HTTPException(status_code=401, detail=f"Invalid JWT Token! Ex: {ex}")
