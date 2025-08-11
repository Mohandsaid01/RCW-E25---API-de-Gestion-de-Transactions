from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, ServiceType, TxStatus

# --- Auth ---
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Clients ---
class ClientCreate(BaseModel):
    name: str
    country: str = "CA"
    document_id: Optional[str] = None

class ClientOut(BaseModel):
    id: int
    name: str
    country: str
    document_id: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# --- Transactions ---
class TxBase(BaseModel):
    client_id: int
    service: ServiceType
    amount: float
    currency: str = "CAD"
    tx_number: str
    status: TxStatus = TxStatus.pending

class TxCreate(TxBase):
    pass

class TxOut(BaseModel):
    id: int
    client_id: int
    service: ServiceType
    amount: float
    currency: str
    tx_number: str
    status: TxStatus
    created_by: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- Search params ---
class TxSearchParams(BaseModel):
    client_name: Optional[str] = None
    service: Optional[ServiceType] = None
    status: Optional[TxStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    page: int = 1
    size: int = 20

# --- Exchange rates ---
class RateCreate(BaseModel):
    base_currency: str = "CAD"
    quote_currency: str
    rate: float

class RateOut(BaseModel):
    id: int
    base_currency: str
    quote_currency: str
    rate: float
    effective_at: datetime
    class Config:
        from_attributes = True

# --- Reports ---
class SummaryOut(BaseModel):
    by_service: dict
    by_currency: dict
    by_country: dict
    total_in_base_currency: float
    base_currency: str

# --- Receipts ---
class ReceiptJSON(BaseModel):
    transaction: TxOut
    client: ClientOut
