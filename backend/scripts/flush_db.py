"""
flush_db.py — Wipe all rows from every table in the database.

Usage (from backend/):
    python -m scripts.flush_db
    python -m scripts.flush_db --confirm   # skip the interactive prompt
"""

import argparse
import sys

from sqlalchemy import text

import models  # noqa: F401 — registers all models with Base
from core.database import Base, engine


def flush(confirmed: bool = False) -> None:
    tables = [t.name for t in reversed(Base.metadata.sorted_tables)]

    if not confirmed:
        print("WARNING: This will permanently delete ALL data from the following tables:")
        for name in tables:
            print(f"  - {name}")
        answer = input("\nType 'yes' to continue: ").strip().lower()
        if answer != "yes":
            print("Aborted.")
            sys.exit(0)

    with engine.begin() as conn:
        # TRUNCATE all tables in dependency order, restarting identity sequences
        table_list = ", ".join(f'"{t}"' for t in tables)
        conn.execute(text(f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE;"))

    print(f"Flushed {len(tables)} table(s): {', '.join(tables)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flush all data from the database.")
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip the interactive confirmation prompt.",
    )
    args = parser.parse_args()
    flush(confirmed=args.confirm)
