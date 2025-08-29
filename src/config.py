from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    gmail_user: str = os.getenv("GMAIL_USER", "")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    embeddings_model: str = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
    reply_model: str = os.getenv("REPLY_MODEL", "gpt-4o-mini")
    db_path: str = os.getenv("DB_PATH", "email_agent.db")
    dry_run: bool = os.getenv("DRY_RUN", "true").lower() == "true"

settings = Settings()
