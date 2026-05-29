# app/routers/crops.py
from datetime import date
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.security import get_current_user
from app.schemas import CropCreate
from app.models import Crop, User

router = APIRouter(prefix="/crops", tags=["crops"])

@router.get("")
def list_crops(s: Session = Depends(get_session), _: User = Depends(get_current_user)):
    return s.exec(select(Crop)).all()

@router.post("", status_code=201)
def create_crop(data: CropCreate, s: Session = Depends(get_session),
                _: User = Depends(get_current_user)):
    crop = Crop(cabin_id=data.cabin_id, species=data.species, planted_at=date.today())
    s.add(crop); s.commit(); s.refresh(crop)
    return crop
