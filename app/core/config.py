from pydantic_settings import BaseSettings
from pydantic import model_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "CRM Platform"
    SECRET_KEY: str = "supersecretkey"  # override via SECRET_KEY env var in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # ── Database ───────────────────────────────────────────────────────────
    # Render automatically sets DATABASE_URL for Postgres add-ons.
    # If DATABASE_URL is provided it takes priority over SQLALCHEMY_DATABASE_URI.
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./crm.db"
    DATABASE_URL: str = ""  # Render Postgres: postgres://... or postgresql://...

    # ── Server port (Render injects $PORT) ────────────────────────────────
    PORT: int = 8000

    # ── Demo mode (set True only for local demos) ──────────────────────────
    DEMO_MODE: bool = False

    # ── Email (SMTP) — leave empty to disable ─────────────────────────────
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "CRM Platform"

    # ── WhatsApp (Twilio) — leave empty to disable ─────────────────────────
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = ""    # e.g. "whatsapp:+14155238886"

    @model_validator(mode="after")
    def _apply_database_url(self) -> "Settings":
        """
        If Render (or any host) provides DATABASE_URL, use it as the
        SQLAlchemy URI. Render uses the postgres:// scheme; SQLAlchemy
        requires postgresql://, so we fix that automatically.
        """
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            self.SQLALCHEMY_DATABASE_URI = url
        return self

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"               # silently ignore unknown env vars

settings = Settings()

