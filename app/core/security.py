# app/core/security.py
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session
from app.core.config import settings
from app.core.database import get_session
from app.models import User, UserRole

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ---- Pratica 1: hash de senha (BCrypt) ----
def hash_password(plain: str) -> str:
    return pwd.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)

# ---- Pratica 2: JWT (HS256, exp 1h, claims com role) ----
def create_access_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user.id), "email": user.email,
               "role": user.role.value, "exp": expire}
    return jwt.encode(payload, settings.jwt_key, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme),
                     s: Session = Depends(get_session)) -> User:
    exc = HTTPException(401, "Token invalido", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.jwt_key, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise exc
    user = s.get(User, user_id)
    if not user:
        raise exc
    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.admin:
        raise HTTPException(403, "Requer permissao de admin")
    return user
