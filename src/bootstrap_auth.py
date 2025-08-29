"""One-time OAuth bootstrap for Gmail API.

Usage:
    python -m src.bootstrap_auth

Places token.json in project root after browser flow.
"""
from __future__ import annotations
from .gmail_client import GmailClient  # noqa: F401


def main() -> None:  # pragma: no cover
    GmailClient()  # building client performs auth
    print("OAuth completed. token.json created/updated.")


if __name__ == "__main__":  # pragma: no cover
    main()
