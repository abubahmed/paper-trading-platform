"""
seed_db.py — Populate the database with realistic dummy data for development.

Creates:
  - 1 active competition (Spring 2025)
  - 5 dummy users (Princeton students)
  - 1 account per user enrolled in the competition
  - 1 balance per account seeded with the competition's initial cash

Usage (from backend/):
    python -m scripts.seed_db
    python -m scripts.seed_db --flush   # flush first, then seed
"""

import argparse
import uuid
from datetime import datetime, timezone

import models  # noqa: F401 — registers all models with Base
from core.database import Base, engine, SessionLocal
from models.user import User
from models.competition import Competition
from models.account import Account
from models.balance import Balance


# ---------------------------------------------------------------------------
# Dummy data
# ---------------------------------------------------------------------------

COMPETITION = {
    "name": "Spring 2025",
    "description": "Princeton Trading Club — Spring 2025 paper trading competition. May the best portfolio win.",
    "start_time": datetime(2025, 3, 1, 9, 30, tzinfo=timezone.utc),
    "end_time": datetime(2025, 5, 15, 16, 0, tzinfo=timezone.utc),
    "initial_cash": 100_000.00,
    "is_active": True,
}

USERS = [
    {
        "clerk_id": "user_seed_001",
        "first_name": "Alice",
        "last_name": "Chen",
        "email": "achen@princeton.edu",
        "username": "achen",
        "netid": "ac001",
        "class_year": 2026,
    },
    {
        "clerk_id": "user_seed_002",
        "first_name": "Ben",
        "last_name": "Okafor",
        "email": "bokafor@princeton.edu",
        "username": "bokafor",
        "netid": "bo002",
        "class_year": 2025,
    },
    {
        "clerk_id": "user_seed_003",
        "first_name": "Clara",
        "last_name": "Reyes",
        "email": "creyes@princeton.edu",
        "username": "creyes",
        "netid": "cr003",
        "class_year": 2027,
    },
    {
        "clerk_id": "user_seed_004",
        "first_name": "David",
        "last_name": "Park",
        "email": "dpark@princeton.edu",
        "username": "dpark",
        "netid": "dp004",
        "class_year": 2026,
    },
    {
        "clerk_id": "user_seed_005",
        "first_name": "Eva",
        "last_name": "Lindström",
        "email": "elindstrom@princeton.edu",
        "username": "elindstrom",
        "netid": "el005",
        "class_year": 2025,
    },
]


# ---------------------------------------------------------------------------
# Seed logic
# ---------------------------------------------------------------------------


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Competition
        competition = Competition(**COMPETITION)
        db.add(competition)
        db.flush()  # get competition.id before committing

        # Users + Accounts + Balances
        for user_data in USERS:
            user = User(**user_data)
            db.add(user)
            db.flush()

            account = Account(user_id=user.id, competition_id=competition.id)
            db.add(account)
            db.flush()

            balance = Balance(
                account_id=account.id,
                available_amount=competition.initial_cash,
                reserved_amount=0,
            )
            db.add(balance)

        db.commit()
        print(f"Seeded competition: '{competition.name}'")
        print(f"Seeded {len(USERS)} users, each with an account and ${competition.initial_cash:,.2f} starting balance.")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def flush() -> None:
    from scripts.flush_db import flush as flush_db

    flush_db(confirmed=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database with dummy development data.")
    parser.add_argument(
        "--flush",
        action="store_true",
        help="Flush all data before seeding (no prompt).",
    )
    args = parser.parse_args()

    if args.flush:
        flush()

    seed()
