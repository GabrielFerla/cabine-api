# app/services/alert_service.py
from sqlmodel import Session
from app.models import Alert, AlertSeverity, CropStatus, Sensor
from app.repositories import alert_repository as alerts

# (especie, tipo_sensor) -> (min, max, critico_min, critico_max)
THRESHOLDS = {
    ("alface",     "umid_solo"): (40, 80, 30, 90),
    ("alface",     "ph"):        (5.5, 6.5, 5.0, 7.0),
    ("alface",     "temp_ar"):   (15, 24, 10, 30),
    ("manjericao", "umid_solo"): (45, 80, 35, 90),
    ("manjericao", "ph"):        (6.0, 7.0, 5.5, 7.5),
    ("manjericao", "temp_ar"):   (18, 28, 12, 33),
    # co2 / luminosidade / ec ficam extensiveis (sem regra no MVP)
}

def get_threshold(species: str, sensor_type: str):
    return THRESHOLDS.get((species, sensor_type))

def evaluate(s: Session, sensor: Sensor, value: float) -> Alert | None:
    cabin = sensor.cabin
    crop = next((c for c in cabin.crops
                 if c.status in (CropStatus.germinacao, CropStatus.crescimento)), None)
    if crop is None:
        return None
    t = get_threshold(crop.species.value, sensor.type.value)
    if t is None:
        return None
    lo, hi, clo, chi = t
    if value < lo or value > hi:
        critical = value < clo or value > chi
        alert = Alert(
            cabin_id=cabin.id, sensor_id=sensor.id,
            severity=AlertSeverity.critical if critical else AlertSeverity.warning,
            message=f"{sensor.type.value} fora do range para {crop.species.value}: "
                    f"{value}{sensor.unit}",
        )
        return alerts.create(s, alert)
    return None
