# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from app.models import CabinType, CabinStatus, CropSpecies

class RegisterIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)     # 72 = limite do bcrypt

class CabinCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    location: str = Field(min_length=1, max_length=255)
    type: CabinType

class CabinUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    location: str = Field(min_length=1, max_length=255)
    status: CabinStatus

class CabinOut(BaseModel):
    id: int
    name: str
    location: str
    type: str
    status: str
    sensor_count: int
    critical_alerts: int

class ReadingCreate(BaseModel):
    sensor_id: int = Field(gt=0)
    value: float

class CropCreate(BaseModel):
    cabin_id: int = Field(gt=0)
    species: CropSpecies
