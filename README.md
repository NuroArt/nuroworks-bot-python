# NuroWorks Bot

A Telegram bot that handles lead capture and product enquiries for NuroWorks:
menu-driven browsing of services and products, delivery of a lead magnet, and
automated follow-up messaging to users who go quiet.

## What it does

- **Inline keyboard navigation** — services, products, and detail views built
  from callback queries rather than slash commands.
- **Lead magnet delivery** — sends the 25-Point Brand Identity Checklist and
  records that it was delivered.
- **Scheduled follow-ups** — a job queue checks for users who received the
  checklist but didn't act, and re-engages them after a delay.
- **SQLite persistence** — users and events are stored locally; follow-up
  eligibility is a query, not in-memory state.
- **Handoff to a human** — a path out of the automated flow.

## Structure

| File | Role |
|---|---|
| `bot.py` | Handlers, keyboards, job scheduling (213 lines, 3 async handlers) |
| `config.py` | All user-facing copy, prices, and links — no logic |
| `storage.py` | SQLite layer: `init_db`, `touch_user`, `mark_event`, `get_user`, `users_needing_followup` |

Copy is isolated in `config.py` so wording and pricing can change without
touching the bot logic.

## Running it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then add your real token
export TELEGRAM_BOT_TOKEN=...    # Windows: set TELEGRAM_BOT_TOKEN=...

python bot.py
```

The database is created automatically on first run.

## Notes

The bot token is read from the `TELEGRAM_BOT_TOKEN` environment variable and is
never stored in the repository. `nuroworks_bot.db` holds real user chat IDs and
is gitignored.

## Stack

Python 3.10 · python-telegram-bot 21.6 (job-queue) · SQLite
