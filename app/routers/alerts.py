# app/routers/alerts.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import get_current_user
from app.repositories import alert_repository as repo
from app.models import User, AlertSeverity

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
def list_alerts(severity: Optional[AlertSeverity] = None,
                resolved: Optional[bool] = None,
                s: Session = Depends(get_session),
                _: User = Depends(get_current_user)):
    return repo.get_all(s, severity, resolved)

@router.put("/{alert_id}/resolve")
def resolve_alert(alert_id: int, s: Session = Depends(get_session),
                  _: User = Depends(get_current_user)):
    a = repo.get_by_id(s, alert_id)
    if not a:
        raise HTTPException(404, "alerta nao encontrado")
    a.resolved = True
    return repo.update(s, a)
