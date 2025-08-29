from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .gmail_client import GmailClient
from .classifier import HybridClassifier
from .reply_generator import ReplyGenerator
from .config import settings
from .priority import compute_priority
from . import storage

@dataclass
class ProcessedEmail:
    id: str
    label: str
    reply_draft: str | None

class Orchestrator:
    def __init__(self) -> None:
        storage.init_db()
        self.gmail = GmailClient()
        self.classifier = HybridClassifier()
        self.replier = ReplyGenerator(
            settings.reply_model, settings.openai_api_key
        )

    def run_once(
        self, *, max_messages: int = 20, draft_replies: bool = True
    ) -> List[ProcessedEmail]:
        processed: List[ProcessedEmail] = []
        messages = self.gmail.list_messages(max_results=max_messages)
        for msg in messages:
            classification = self.classifier.classify(
                msg.subject, msg.body_text
            )
            priority = compute_priority(classification.label)
            reply_draft = None
            if draft_replies and classification.label in {"ACTION", "MEETING", "WORK"}:
                reply_draft = self.replier.draft_reply(
                    msg.from_, msg.subject, msg.body_text[:4000]
                )
            storage.upsert_email(
                message_id=msg.id,
                thread_id=msg.thread_id,
                subject=msg.subject,
                from_addr=msg.from_,
                label=classification.label,
                priority=priority,
                draft_reply=reply_draft,
            )
            processed.append(
                ProcessedEmail(
                    id=msg.id, label=classification.label, reply_draft=reply_draft
                )
            )
        return processed
