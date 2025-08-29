# EmailAgent

An automated email agent for Gmail to:

* Fetch & sync messages
* Classify / categorize emails (e.g. Work, Personal, Promotions, Finance, Action Needed, Meetings)
* Prioritize & sort
* Draft smart replies (human-in-the-loop approval optional)
* (Future) Auto-send approved replies

## High-Level Architecture

Components:

* GmailClient: Wrapper around Gmail REST API (list, get, send, modify labels)
* VectorStore / Embeddings: For semantic similarity & classification support
* Classifier: Rule + ML hybrid classifier
* ReplyGenerator: LLM-backed reply drafting with context window management
* Orchestrator: Coordinates fetch -> classify -> propose reply -> persist
* Storage: Local SQLite (emails metadata, labels, status, drafts)

## Tech Stack (proposed)

* Python 3.11+
* google-api-python-client (Gmail API)
* google-auth / google-auth-oauthlib for OAuth
* sqlite3 (standard lib) or SQLModel / SQLAlchemy for abstraction
* sentence-transformers (MiniLM) for embeddings OR OpenAI embeddings (optional)
* openai (optional) for advanced reply drafting

## Security & Privacy

* OAuth tokens stored only locally (`token.json`, do **NOT** commit)
* `.env` for API keys
* Minimal scopes: `https://www.googleapis.com/auth/gmail.modify`

## Setup

1. Create a Google Cloud project & enable Gmail API
2. Configure OAuth consent screen (Internal if only you)
3. Create OAuth Client ID (Desktop) and download `credentials.json` into project root.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run initial auth & fetch (script to be added):

```bash
python -m src.bootstrap_auth
```

## Running the Agent (prototype loop)

```bash
python -m src.run_once --max 25 --draft-replies
```

## Environment Variables (.env)

```env
OPENAI_API_KEY=...            # if using OpenAI
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
REPLY_MODEL=gpt-4o-mini       # or local
```

## Roadmap

* [ ] OAuth bootstrap script
* [x] Gmail fetcher (basic)
* [ ] SQLite models
* [x] Hybrid classifier (rule-based MVP)
* [x] Reply generator (fallback + OpenAI option)
* [x] Orchestrator loop
* [x] CLI flags & config
* [ ] Basic tests
* [ ] Logging & metrics
* [ ] Auto-send with safety checks

## Disclaimer

This is a personal productivity tool. Use responsibly; always review AI-drafted replies before sending.
