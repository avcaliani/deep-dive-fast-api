from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

SECRET_KEY = settings.TOKEN_SECRET_KEY
ALGORITHM = settings.TOKEN_ALGORITHM
EXPIRE_MINUTES = settings.TOKEN_EXPIRE_MINUTES

EXCEPTION_INVALID_CREDENTIALS = HTTPException(
    status_code=401,
    detail="Invalid credentials!",
    headers={"WWW-Authenticate": "Bearer"},
)
CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return CONTEXT.hash(password)


def check_password(plain: str, hashed: str) -> bool:
    return CONTEXT.verify(plain, hashed)


def create_token(subject: str, mood: str):
    data = {"sub": subject, "mood": mood, "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)}
    return {"token": jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}


def decode(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as ex:
        raise HTTPException(status_code=401, detail=f"Invalid JWT Token! Ex: {ex}")
