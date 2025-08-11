from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
from app.deps import get_db, require_roles
from app.models import Transaction, Client, UserRole, ExchangeRate
from app.core.config import settings
from app.schemas import SummaryOut

router = APIRouter(prefix="/reports", tags=["Reports"])

def to_base_currency(db: Session, amount: float, currency: str) -> float:
    base = settings.default_base_currency
    if currency == base:
        return amount
    # on prend le dernier taux disponible base->currency ou currency->base
    rate = db.query(ExchangeRate).filter(
        ExchangeRate.base_currency == base,
        ExchangeRate.quote_currency == currency
    ).order_by(ExchangeRate.effective_at.desc()).first()
    if rate:
        # si base->currency (ex CAD->USD) et amount est en USD, alors amount_en_base = amount / rate
        return amount / rate.rate
    # essai inverse
    inv = db.query(ExchangeRate).filter(
        ExchangeRate.base_currency == currency,
        ExchangeRate.quote_currency == base
    ).order_by(ExchangeRate.effective_at.desc()).first()
    if inv:
        return amount * inv.rate
    # pas de taux => on laisse inchangé (fallback)
    return amount

@router.get("/summary", response_model=SummaryOut, dependencies=[Depends(require_roles(UserRole.supervisor, UserRole.admin))])
def summary(db: Session = Depends(get_db)):
    # by_service
    rows = db.query(Transaction.service, func.sum(Transaction.amount), Transaction.currency).group_by(Transaction.service, Transaction.currency).all()
    by_service: Dict[str, float] = {}
    total_base = 0.0
    for service, sum_amount, currency in rows:
        key = service.value
        by_service[key] = by_service.get(key, 0.0) + float(sum_amount)
        total_base += to_base_currency(db, float(sum_amount), currency)

    # by_currency
    rows_c = db.query(Transaction.currency, func.sum(Transaction.amount)).group_by(Transaction.currency).all()
    by_currency = {c: float(s) for c, s in rows_c}

    # by_country (via Client)
    rows_country = db.query(Client.country, func.sum(Transaction.amount)).join(Client, Transaction.client_id == Client.id).group_by(Client.country).all()
    by_country = {country: float(s) for country, s in rows_country}

    return SummaryOut(
        by_service=by_service,
        by_currency=by_currency,
        by_country=by_country,
        total_in_base_currency=round(total_base, 2),
        base_currency=settings.default_base_currency
    )
