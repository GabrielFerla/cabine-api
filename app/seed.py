# app/seed.py
import random
from datetime import timedelta
from sqlmodel import Session, select
from app.core.database import engine
from app.core.security import hash_password
from app.models import (User, Cabin, Sensor, Reading, Alert, Crop,
                         UserRole, CabinType, SensorType, AlertSeverity,
                         CropSpecies, CropStatus, utcnow)

def seed():
    with Session(engine) as s:
        if s.exec(select(User)).first():
            return                                          # idempotente

        admin = User(name="Gabriel", email="admin@cabine.dev",
                     password_hash=hash_password("senha123"), role=UserRole.admin)
        s.add(admin); s.commit(); s.refresh(admin)

        helio = Cabin(user_id=admin.id, name="Heliopolis-01",
                      location="Heliopolis, SP", type=CabinType.terrestre)
        lunar = Cabin(user_id=admin.id, name="Lunar-Base-Artemis",
                      location="Mare Tranquillitatis", type=CabinType.espacial)
        s.add(helio); s.add(lunar); s.commit(); s.refresh(helio); s.refresh(lunar)

        tipos = [(SensorType.temp_ar, "C"), (SensorType.umid_solo, "%"),
                 (SensorType.ph, "pH"), (SensorType.ec, "mS/cm"),
                 (SensorType.luminosidade, "lux"), (SensorType.co2, "ppm")]
        sensores = []
        for cab in (helio, lunar):
            for t, u in tipos:
                sensor = Sensor(cabin_id=cab.id, type=t, unit=u)
                s.add(sensor); sensores.append(sensor)
        s.commit()
        for sensor in sensores:
            s.refresh(sensor)

        rnd = random.Random(42)
        for sensor in sensores:
            for i in range(8):
                v = {
                    SensorType.temp_ar:      20 + rnd.random() * 8,
                    SensorType.umid_solo:    30 + rnd.random() * 50,
                    SensorType.ph:           5.5 + rnd.random(),
                    SensorType.ec:           1.2 + rnd.random(),
                    SensorType.luminosidade: rnd.randint(50, 16000),
                    SensorType.co2:          rnd.randint(400, 1400),
                }[sensor.type]
                s.add(Reading(sensor_id=sensor.id, value=round(v, 2),
                              read_at=utcnow() - timedelta(hours=i)))

        s.add(Crop(cabin_id=helio.id, species=CropSpecies.alface,
                   planted_at=(utcnow() - timedelta(days=12)).date(),
                   status=CropStatus.crescimento))
        s.add(Crop(cabin_id=lunar.id, species=CropSpecies.manjericao,
                   planted_at=(utcnow() - timedelta(days=5)).date(),
                   status=CropStatus.germinacao))

        s.add(Alert(cabin_id=helio.id, severity=AlertSeverity.critical,
                    message="Umidade do solo abaixo de 30%"))
        s.add(Alert(cabin_id=helio.id, severity=AlertSeverity.warning,
                    message="pH se aproximando do limite inferior"))
        s.add(Alert(cabin_id=lunar.id, severity=AlertSeverity.info,
                    message="Cabine inicializada"))
        s.commit()
