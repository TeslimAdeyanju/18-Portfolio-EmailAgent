from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Text,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

Base = declarative_base()


class EmailRecord(Base):  # type: ignore
    __tablename__ = "emails"
    id = Column(String, primary_key=True)
    thread_id = Column(String, index=True)
    subject = Column(String, index=True)
    from_addr = Column(String, index=True)
    label = Column(String, index=True)
    priority = Column(Integer, index=True, default=0)
    draft_reply = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    replied = Column(Boolean, default=False)


def get_engine():
    return create_engine(f"sqlite:///{settings.db_path}", future=True, echo=False)


Engine = get_engine()
SessionLocal = sessionmaker(bind=Engine, expire_on_commit=False, autoflush=False)


def init_db() -> None:
    Base.metadata.create_all(Engine)


def upsert_email(
    *,
    message_id: str,
    thread_id: str,
    subject: str,
    from_addr: str,
    label: str,
    priority: int,
    draft_reply: str | None,
) -> None:
    session = SessionLocal()
    try:
        rec = session.get(EmailRecord, message_id)
        if not rec:
            rec = EmailRecord(
                id=message_id,
                thread_id=thread_id,
                subject=subject[:500],
                from_addr=from_addr[:320],
                label=label,
                priority=priority,
                draft_reply=draft_reply,
            )
            session.add(rec)
        else:
            rec.label = label
            rec.priority = priority
            if draft_reply:
                rec.draft_reply = draft_reply
        session.commit()
    finally:
        session.close()
