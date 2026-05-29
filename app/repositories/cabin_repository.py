# app/repositories/cabin_repository.py
from sqlmodel import Session, select
from app.models import Cabin

def get_all(s: Session): return s.exec(select(Cabin)).all()
def get_by_id(s: Session, id: int): return s.get(Cabin, id)
def create(s: Session, c: Cabin): s.add(c); s.commit(); s.refresh(c); return c
def update(s: Session, c: Cabin): s.add(c); s.commit(); s.refresh(c); return c
def delete(s: Session, c: Cabin): s.delete(c); s.commit()
