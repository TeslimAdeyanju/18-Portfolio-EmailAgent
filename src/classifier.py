from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import re

BASIC_LABELS = [
    "WORK",
    "PERSONAL",
    "PROMOTIONS",
    "FINANCE",
    "ACTION",
    "MEETING",
    "OTHER",
]

KEYWORD_RULES = [
    (re.compile(r"invoice|receipt|payment", re.I), "FINANCE"),
    (re.compile(r"meeting|call|schedule|calendar", re.I), "MEETING"),
    (re.compile(r"unsubscribe|sale|discount|offer", re.I), "PROMOTIONS"),
    (re.compile(r"urgent|asap|action required|follow up", re.I), "ACTION"),
]

@dataclass
class ClassifiedEmail:
    label: str
    confidence: float
    reasons: List[str]

class HybridClassifier:
    def classify(self, subject: str, body: str) -> ClassifiedEmail:
        text = f"{subject}\n{body}"[:8000]
        reasons: List[str] = []
        for pattern, label in KEYWORD_RULES:
            if pattern.search(text):
                reasons.append(f"Matched rule: {label}")
                return ClassifiedEmail(label=label, confidence=0.85, reasons=reasons)
        # fallback naive heuristics
        if len(body) < 40:
            return ClassifiedEmail(label="ACTION", confidence=0.55, reasons=["Short body heuristic"])
        return ClassifiedEmail(label="OTHER", confidence=0.4, reasons=["No rule matched"])
