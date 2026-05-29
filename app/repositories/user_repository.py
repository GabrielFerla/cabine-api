# app/repositories/user_repository.py
from sqlmodel import Session, select
from app.models import User

def get_by_email(s: Session, email: str):
    return s.exec(select(User).where(User.email == email)).first()

def get_by_id(s: Session, id: int):
    return s.get(User, id)

def create(s: Session, u: User):
    s.add(u); s.commit(); s.refresh(u); return u
