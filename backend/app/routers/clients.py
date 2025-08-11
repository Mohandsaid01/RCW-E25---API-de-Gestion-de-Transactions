from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.deps import get_db, require_roles
from app.models import Client, UserRole
from app.schemas import ClientCreate, ClientOut

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("", response_model=ClientOut, dependencies=[Depends(require_roles(UserRole.agent, UserRole.supervisor, UserRole.admin))])
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(name=payload.name, country=payload.country, document_id=payload.document_id)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("", response_model=List[ClientOut], dependencies=[Depends(require_roles(UserRole.agent, UserRole.supervisor, UserRole.admin))])
def list_clients(q: str = Query(default=None, description="Recherche par nom"), db: Session = Depends(get_db)):
    qry = db.query(Client)
    if q:
        qry = qry.filter(Client.name.ilike(f"%{q}%"))
    return qry.order_by(Client.id.desc()).limit(100).all()
