from __future__ import annotations
import argparse
from .orchestrator import Orchestrator
from rich import print


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=10)
    parser.add_argument("--draft-replies", action="store_true")
    args = parser.parse_args()

    orch = Orchestrator()
    results = orch.run_once(max_messages=args.max, draft_replies=args.draft_replies)
    for r in results:
        print({"id": r.id, "label": r.label, "reply_preview": (r.reply_draft or "")[:120]})


if __name__ == "__main__":
    main()
