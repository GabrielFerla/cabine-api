# app/models.py
from datetime import datetime, date, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

# ---------- enums ----------
class UserRole(str, Enum):
    admin = "admin"; operator = "operator"; viewer = "viewer"

class CabinType(str, Enum):
    terrestre = "terrestre"; espacial = "espacial"          # chave da narrativa hibrida

class CabinStatus(str, Enum):
    active = "active"; maintenance = "maintenance"; inactive = "inactive"

class SensorType(str, Enum):
    temp_ar = "temp_ar"; umid_solo = "umid_solo"; ph = "ph"; ec = "ec"
    luminosidade = "luminosidade"; co2 = "co2"; camera_visao = "camera_visao"

class SensorStatus(str, Enum):
    active = "active"; offline = "offline"; error = "error"

class AlertSeverity(str, Enum):
    info = "info"; warning = "warning"; critical = "critical"

class CropSpecies(str, Enum):
    alface = "alface"; manjericao = "manjericao"; rucula = "rucula"
    microgreen = "microgreen"; salsa = "salsa"; tomate_cereja = "tomate_cereja"

class CropStatus(str, Enum):
    germinacao = "germinacao"; crescimento = "crescimento"
    maduro = "maduro"; colhido = "colhido"; perdido = "perdido"

# ---------- tabelas ----------
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=120)
    email: str = Field(max_length=160, unique=True, index=True)
    password_hash: str = Field(max_length=120)             # NUNCA a senha pura
    role: UserRole = Field(default=UserRole.viewer)
    created_at: datetime = Field(default_factory=utcnow)
    cabins: List["Cabin"] = Relationship(back_populates="user")

class Cabin(SQLModel, table=True):
    __tablename__ = "cabins"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str = Field(max_length=120)                      # "Heliopolis-01", "Lunar-Base-Artemis"
    location: str = Field(max_length=255)
    type: CabinType
    installed_at: datetime = Field(default_factory=utcnow)
    status: CabinStatus = Field(default=CabinStatus.active)
    user: Optional[User] = Relationship(back_populates="cabins")
    sensors: List["Sensor"] = Relationship(back_populates="cabin")
    crops: List["Crop"] = Relationship(back_populates="cabin")
    alerts: List["Alert"] = Relationship(back_populates="cabin")

class Sensor(SQLModel, table=True):
    __tablename__ = "sensors"
    id: Optional[int] = Field(default=None, primary_key=True)
    cabin_id: int = Field(foreign_key="cabins.id", index=True)
    type: SensorType
    unit: str = Field(max_length=20)                       # "C", "%", "ppm"
    status: SensorStatus = Field(default=SensorStatus.active)
    cabin: Optional[Cabin] = Relationship(back_populates="sensors")
    readings: List["Reading"] = Relationship(back_populates="sensor")

class Reading(SQLModel, table=True):
    __tablename__ = "readings"                             # so sensores NUMERICOS
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensors.id", index=True)
    value: Decimal = Field(max_digits=10, decimal_places=2)
    read_at: datetime = Field(default_factory=utcnow, index=True)
    sensor: Optional[Sensor] = Relationship(back_populates="readings")

class Alert(SQLModel, table=True):
    __tablename__ = "alerts"
    id: Optional[int] = Field(default=None, primary_key=True)
    cabin_id: int = Field(foreign_key="cabins.id", index=True)
    sensor_id: Optional[int] = Field(default=None, foreign_key="sensors.id")
    severity: AlertSeverity
    message: str = Field(max_length=255)
    triggered_at: datetime = Field(default_factory=utcnow)
    resolved: bool = Field(default=False)
    cabin: Optional[Cabin] = Relationship(back_populates="alerts")

class Crop(SQLModel, table=True):
    __tablename__ = "crops"
    id: Optional[int] = Field(default=None, primary_key=True)
    cabin_id: int = Field(foreign_key="cabins.id")
    species: CropSpecies
    planted_at: date
    status: CropStatus = Field(default=CropStatus.germinacao)
    cabin: Optional[Cabin] = Relationship(back_populates="crops")
