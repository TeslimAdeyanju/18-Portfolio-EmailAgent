from __future__ import annotations
from typing import Optional
import textwrap
import os

try:
    import openai  # type: ignore
except ImportError:  # pragma: no cover
    openai = None  # type: ignore

SYSTEM_PROMPT = "You are a concise email assistant. Write polite, clear professional replies."

class ReplyGenerator:
    def __init__(self, model: str, api_key: Optional[str]):
        self.model = model
        self.api_key = api_key
        if openai and api_key:
            openai.api_key = api_key

    def draft_reply(self, original_from: str, subject: str, body: str) -> str:
        if not openai or not self.api_key:
            # fallback simple template
            snippet = body[:300].replace("\n", " ")
            return textwrap.dedent(
                f"""Hi {original_from.split('<')[0].strip(',')},\n\nThanks for your email regarding '{subject}'. I will review and get back to you shortly.\n\nBest,\nTeslim"""
            ).strip()
        prompt = f"Original email from {original_from} about '{subject}':\n\n{body}\n\nDraft a helpful reply."[:6000]
        try:
            resp = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=300,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:  # pragma: no cover - network
            return f"[Fallback Reply] Thank you for your email about '{subject}'. I'll follow up soon. ({e})"
