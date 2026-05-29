# app/repositories/alert_repository.py
from typing import Optional
from sqlmodel import Session, select
from app.models import Alert, AlertSeverity

def create(s: Session, a: Alert):
    s.add(a); s.commit(); s.refresh(a); return a

def get_all(s: Session, severity: Optional[AlertSeverity] = None,
            resolved: Optional[bool] = None):
    q = select(Alert)
    if severity is not None:
        q = q.where(Alert.severity == severity)
    if resolved is not None:
        q = q.where(Alert.resolved == resolved)
    return s.exec(q.order_by(Alert.triggered_at)).all()

def get_by_id(s: Session, id: int):
    return s.get(Alert, id)

def update(s: Session, a: Alert):
    s.add(a); s.commit(); s.refresh(a); return a
