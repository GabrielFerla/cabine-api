# app/services/cabin_service.py
from sqlmodel import Session
from app.repositories import cabin_repository as repo
from app.models import Cabin, AlertSeverity
from app.schemas import CabinCreate, CabinUpdate, CabinOut

def _to_out(c: Cabin) -> CabinOut:
    return CabinOut(
        id=c.id, name=c.name, location=c.location,
        type=c.type.value, status=c.status.value,
        sensor_count=len(c.sensors),
        critical_alerts=sum(1 for a in c.alerts
                            if a.severity == AlertSeverity.critical and not a.resolved),
    )

def list_cabins(s: Session): return [_to_out(c) for c in repo.get_all(s)]

def get_cabin(s: Session, id: int):
    c = repo.get_by_id(s, id)
    return _to_out(c) if c else None

def create_cabin(s: Session, data: CabinCreate, user_id: int):
    c = Cabin(name=data.name, location=data.location, type=data.type, user_id=user_id)
    return _to_out(repo.create(s, c))

def update_cabin(s: Session, id: int, data: CabinUpdate):
    c = repo.get_by_id(s, id)
    if not c: return None
    c.name, c.location, c.status = data.name, data.location, data.status
    return _to_out(repo.update(s, c))

def delete_cabin(s: Session, id: int) -> bool:
    c = repo.get_by_id(s, id)
    if not c: return False
    repo.delete(s, c); return True
