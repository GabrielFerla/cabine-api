# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.core.database import get_session
from app.core.security import hash_password
from app.models import (User, Cabin, Sensor, Crop, UserRole, CabinType,
                        SensorType, CropSpecies, CropStatus)

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        admin = User(name="Admin", email="admin@test.dev",
                     password_hash=hash_password("senha123"), role=UserRole.admin)
        op = User(name="Op", email="op@test.dev",
                  password_hash=hash_password("senha123"), role=UserRole.operator)
        s.add(admin); s.add(op); s.commit(); s.refresh(admin)
        cabin = Cabin(user_id=admin.id, name="Heliopolis-01",
                      location="SP", type=CabinType.terrestre)
        s.add(cabin); s.commit(); s.refresh(cabin)
        s.add(Sensor(cabin_id=cabin.id, type=SensorType.umid_solo, unit="%"))
        s.add(Crop(cabin_id=cabin.id, species=CropSpecies.alface,
                   planted_at=__import__("datetime").date.today(),
                   status=CropStatus.crescimento))
        s.commit()
        yield s

@pytest.fixture(name="client")
def client_fixture(session):
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()

def login(client, email="admin@test.dev", password="senha123") -> str:
    r = client.post("/auth/login", data={"username": email, "password": password})
    return r.json()["access_token"]
