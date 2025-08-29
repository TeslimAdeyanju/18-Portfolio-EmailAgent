from __future__ import annotations
from typing import List, Dict, Any, Optional
import base64
import os
import pickle
from pathlib import Path
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
TOKEN_PATH = Path("token.json")
CREDENTIALS_PATH = Path("credentials.json")

@dataclass
class GmailMessage:
    id: str
    thread_id: str
    snippet: str
    payload: Dict[str, Any]
    labels: List[str]
    internal_date: int
    history_id: str | None = None

    @property
    def subject(self) -> str:
        headers = self.payload.get("headers", [])
        for h in headers:
            if h.get("name", "").lower() == "subject":
                return h.get("value", "")
        return ""

    @property
    def from_(self) -> str:
        for h in self.payload.get("headers", []):
            if h.get("name", "").lower() == "from":
                return h.get("value", "")
        return ""

    @property
    def to(self) -> str:
        for h in self.payload.get("headers", []):
            if h.get("name", "").lower() == "to":
                return h.get("value", "")
        return ""

    @property
    def body_text(self) -> str:
        def decode(part):
            data = part.get("body", {}).get("data")
            if not data:
                return ""
            return base64.urlsafe_b64decode(data.encode()).decode(errors="ignore")
        payload = self.payload
        if "parts" in payload:
            texts = []
            for p in payload["parts"]:
                mime = p.get("mimeType", "")
                if mime.startswith("text/plain"):
                    texts.append(decode(p))
            return "\n".join(texts)
        return decode(payload)

class GmailClient:
    def __init__(self):
        self.service = self._build_service()

    def _build_service(self):
        creds: Optional[Credentials] = None
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_PATH.exists():
                    raise FileNotFoundError("Missing credentials.json for Gmail OAuth.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        return build("gmail", "v1", credentials=creds)

    def list_messages(self, max_results: int = 50, label_ids: Optional[List[str]] = None) -> List[GmailMessage]:
        resp = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=max_results, labelIds=label_ids or [])
            .execute()
        )
        messages = []
        for item in resp.get("messages", []):
            full = (
                self.service.users()
                .messages()
                .get(userId="me", id=item["id"], format="full")
                .execute()
            )
            messages.append(
                GmailMessage(
                    id=full["id"],
                    thread_id=full.get("threadId", ""),
                    snippet=full.get("snippet", ""),
                    payload=full.get("payload", {}),
                    labels=full.get("labelIds", []),
                    internal_date=int(full.get("internalDate", 0)),
                    history_id=full.get("historyId"),
                )
            )
        return messages

    def send_message(self, raw_mime_bytes: bytes) -> dict:
        import base64 as b64
        encoded = b64.urlsafe_b64encode(raw_mime_bytes).decode()
        return (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": encoded})
            .execute()
        )

    def add_labels(self, message_id: str, labels_to_add: list[str]):
        return (
            self.service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body={"addLabelIds": labels_to_add, "removeLabelIds": []},
            )
            .execute()
        )
