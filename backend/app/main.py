from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import Base, engine, SessionLocal
from app.routers import auth, clients, transactions, reports, rates
from app.models import User, UserRole
from app.security import hash_password

app = FastAPI(
    title="RCW-E25 API de Gestion de Transactions",
    version="1.0.0",
    description="API centralisant RIA / Western Union / MoneyGram — recherche, reçus, dashboard, alertes."
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # seed un admin si absent
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email=="admin@rcw.local").first()
        if not admin:
            admin = User(
                email="admin@rcw.local",
                full_name="Admin",
                role=UserRole.admin,
                hashed_password=hash_password("admin123")
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

# Routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(transactions.router)
app.include_router(reports.router)
app.include_router(rates.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
