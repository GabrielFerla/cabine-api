# app/routers/readings.py
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import get_current_user
from app.services import alert_service
from app.schemas import ReadingCreate
from app.models import Reading, Sensor, User

router = APIRouter(prefix="/readings", tags=["readings"])

@router.post("", status_code=201)
def create_reading(data: ReadingCreate, s: Session = Depends(get_session),
                   _: User = Depends(get_current_user)):
    sensor = s.get(Sensor, data.sensor_id)
    if not sensor:
        raise HTTPException(404, "sensor inexistente")
    reading = Reading(sensor_id=sensor.id, value=Decimal(str(data.value)))
    s.add(reading); s.commit(); s.refresh(reading)
    alert = alert_service.evaluate(s, sensor, data.value)   # gera alerta se fora do range
    return {"reading_id": reading.id, "value": float(reading.value),
            "alert_generated": alert is not None,
            "alert_severity": alert.severity.value if alert else None}
