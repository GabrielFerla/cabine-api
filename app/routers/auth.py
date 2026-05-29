# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import hash_password, verify_password, create_access_token
from app.core.ratelimit import limiter
from app.repositories import user_repository as users
from app.models import User, UserRole
from app.schemas import RegisterIn

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
def register(data: RegisterIn, s: Session = Depends(get_session)):
    if users.get_by_email(s, data.email):
        raise HTTPException(409, "E-mail ja cadastrado")
    user = User(name=data.name, email=data.email,
                password_hash=hash_password(data.password), role=UserRole.operator)
    user = users.create(s, user)
    return {"id": user.id, "email": user.email}

# ---- Bonus: rate limit no login (slowapi) ----
@router.post("/login")
@limiter.limit("10/minute")
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(),
          s: Session = Depends(get_session)):
    user = users.get_by_email(s, form.username)            # username = email
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Credenciais invalidas")  # mesma resposta p/ user inexistente
    return {"access_token": create_access_token(user), "token_type": "bearer"}
