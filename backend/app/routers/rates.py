from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db, require_roles
from app.models import ExchangeRate, UserRole
from app.schemas import RateCreate, RateOut

router = APIRouter(prefix="/rates", tags=["Exchange Rates"])

@router.post("", response_model=RateOut, dependencies=[Depends(require_roles(UserRole.supervisor, UserRole.admin))])
def add_rate(payload: RateCreate, db: Session = Depends(get_db)):
    r = ExchangeRate(base_currency=payload.base_currency, quote_currency=payload.quote_currency, rate=payload.rate)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.get("", response_model=List[RateOut], dependencies=[Depends(require_roles(UserRole.agent, UserRole.supervisor, UserRole.admin))])
def list_rates(db: Session = Depends(get_db)):
    return db.query(ExchangeRate).order_by(ExchangeRate.effective_at.desc()).limit(200).all()
