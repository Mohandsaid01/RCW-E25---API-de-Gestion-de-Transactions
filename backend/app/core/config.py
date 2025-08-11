from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://rcw:rcwpass@localhost:5432/rcwdb")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
    jwt_algo: str = os.getenv("JWT_ALGO", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    cors_origins: List[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
    suspicious_amount: float = float(os.getenv("SUSPICIOUS_AMOUNT", "3000"))
    suspicious_window_minutes: int = int(os.getenv("SUSPICIOUS_WINDOW_MINUTES", "30"))
    suspicious_max_tx: int = int(os.getenv("SUSPICIOUS_MAX_TX", "3"))
    default_base_currency: str = os.getenv("DEFAULT_BASE_CURRENCY", "CAD")

settings = Settings()
