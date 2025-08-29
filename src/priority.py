from __future__ import annotations

LABEL_PRIORITY = {
    "ACTION": 100,
    "MEETING": 90,
    "WORK": 80,
    "FINANCE": 60,
    "PERSONAL": 50,
    "PROMOTIONS": 20,
    "OTHER": 10,
}


def compute_priority(label: str) -> int:
    return LABEL_PRIORITY.get(label, 5)
