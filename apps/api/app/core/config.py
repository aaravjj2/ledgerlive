"""LedgerLive core configuration."""
import os

APP_MODE = os.getenv("APP_MODE", "LOCAL")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "DEMO")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./ledgerlive.db")
E2E_MODE = os.getenv("E2E_MODE", "0") == "1"
PROJECT_ID = "LEDGERLIVE"
