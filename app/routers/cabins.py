# app/routers/cabins.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import get_current_user, require_admin
from app.services import cabin_service
from app.schemas import CabinCreate, CabinUpdate, CabinOut
from app.models import User, Cabin, Sensor, Reading

router = APIRouter(prefix="/cabins", tags=["cabins"])

@router.get("", response_model=list[CabinOut])
def list_cabins(s: Session = Depends(get_session), _: User = Depends(get_current_user)):
    return cabin_service.list_cabins(s)

@router.get("/{cabin_id}", response_model=CabinOut)
def get_cabin(cabin_id: int, s: Session = Depends(get_session), _: User = Depends(get_current_user)):
    c = cabin_service.get_cabin(s, cabin_id)
    if not c: raise HTTPException(404, "cabine nao encontrada")
    return c

@router.get("/{cabin_id}/readings")
def list_cabin_readings(cabin_id: int, s: Session = Depends(get_session),
                        _: User = Depends(get_current_user)):
    cabin = s.get(Cabin, cabin_id)
    if not cabin:
        raise HTTPException(404, "cabine nao encontrada")
    sensor_ids = [sensor.id for sensor in cabin.sensors]
    if not sensor_ids:
        return []
    return s.exec(
        select(Reading).where(Reading.sensor_id.in_(sensor_ids))
        .order_by(Reading.read_at.desc())
    ).all()

@router.post("", response_model=CabinOut, status_code=201)
def create_cabin(data: CabinCreate, s: Session = Depends(get_session),
                 admin: User = Depends(require_admin)):
    return cabin_service.create_cabin(s, data, admin.id)

@router.put("/{cabin_id}", response_model=CabinOut)
def update_cabin(cabin_id: int, data: CabinUpdate, s: Session = Depends(get_session),
                 _: User = Depends(require_admin)):
    c = cabin_service.update_cabin(s, cabin_id, data)
    if not c: raise HTTPException(404, "cabine nao encontrada")
    return c

@router.delete("/{cabin_id}", status_code=204)
def delete_cabin(cabin_id: int, s: Session = Depends(get_session),
                 _: User = Depends(require_admin)):
    if not cabin_service.delete_cabin(s, cabin_id):
        raise HTTPException(404, "cabine nao encontrada")
