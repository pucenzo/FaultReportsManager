from passlib.context import CryptContext
from app.core.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Any
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

ALGORITHM = "HS256"

SECRET_KEY = settings.SECRET_KEY

def create_access_token(soggetto: str, ruolo: str, id: int, expires_delta: timedelta) -> str: 
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": soggetto, "role": ruolo, "id": id, "exp": expire}
    encoded_jwt = jwt.encode( 
        to_encode, 
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    ) 
    return encoded_jwt

