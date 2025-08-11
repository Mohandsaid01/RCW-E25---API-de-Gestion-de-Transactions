from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from app.deps import get_db, require_roles, get_current_user
from app.models import Transaction, Client, UserRole, ActionLog, Alert, ServiceType, TxStatus, User
from app.schemas import TxCreate, TxOut
from app.core.config import settings
from app.utils.receipts import build_receipt_json

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("", response_model=TxOut, dependencies=[Depends(require_roles(UserRole.agent, UserRole.supervisor, UserRole.admin))])
def create_transaction(payload: TxCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == payload.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client introuvable")

    tx = Transaction(
        client_id=payload.client_id,
        service=payload.service,
        amount=payload.amount,
        currency=payload.currency,
        tx_number=payload.tx_number,
        status=payload.status,
        created_by=current_user.id
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    # Log
    log = ActionLog(actor_id=current_user.id, action="CREATE_TX", entity="Transaction", entity_id=tx.id, details=f"service={tx.service}, amount={tx.amount}{tx.currency}")
    db.add(log)

    # Alertes simples
    reasons = []
    if tx.amount >= settings.suspicious_amount:
        reasons.append(f"Montant élevé >= {settings.suspicious_amount} {tx.currency}")

    window_start = datetime.now(timezone.utc) - timedelta(minutes=settings.suspicious_window_minutes)
    recent_count = db.query(Transaction).filter(
        Transaction.client_id == tx.client_id,
        Transaction.created_at >= window_start
    ).count()
    if recent_count >= settings.suspicious_max_tx:
        reasons.append(f"Transactions multiples ({recent_count}) en {settings.suspicious_window_minutes} min")

    if reasons:
        alert = Alert(tx_id=tx.id, level="HIGH", reason="; ".join(reasons))
        db.add(alert)

    db.commit()
    return tx

@router.get("", response_model=List[TxOut], dependencies=[Depends(require_roles(UserRole.agent, UserRole.supervisor, UserRole.admin))])
def search_transactions(
    db: Session = Depends(get_db),
    client_name: Optional[str] = None,
    service: Optional[ServiceType] = None,
    status: Optional[TxStatus] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    page: int = 1,
    size: int = 20,
):
    q = db.query(Transaction).join(Client)

    if client_name:
        q = q.filter(Client.name.ilike(f"%{client_name}%"))
    if service:
        q = q.filter(Transaction.service == service)
    if status:
        q = q.filter(Transaction.status == status)
    if date_from:
        q = q.filter(Transaction.created_at >= date_from)
    if date_to:
        q = q.filter(Transaction.created_at <= date_to)
    if min_amount is not None:
        q = q.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        q = q.filter(Transaction.amount <= max_amount)

    q = q.order_by(Transaction.created_at.desc())
    return q.offset((page - 1) * size).limit(size).all()

@router.get("/{tx_id}/receipt.json")
def get_receipt_json(tx_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction introuvable")
    return build_receipt_json(tx)
