"""
test_alpaca.py — Sanity check for the Alpaca snapshot client.

Fetches the latest price snapshot for 30 popular symbols, prints a
clean summary, and writes the raw response to backend/data/snapshots.json.

Usage (from backend/):
    uv run test-alpaca
    python -m scripts.test_alpaca
"""

import json
from pathlib import Path
from services.alpaca import get_snapshots

SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
    "BRK.B",
    "JPM",
    "V",
    "UNH",
    "XOM",
    "LLY",
    "JNJ",
    "WMT",
    "MA",
    "PG",
    "ORCL",
    "HD",
    "AVGO",
    "CVX",
    "MRK",
    "KO",
    "PEP",
    "ABBV",
    "COST",
    "BAC",
    "MCD",
    "ADBE",
    "SPY",
]

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "snapshots.json"


if __name__ == "__main__":
    print(f"Fetching snapshots for: {', '.join(SYMBOLS)}\n")

    data = get_snapshots(SYMBOLS)

    for symbol in SYMBOLS:
        snapshot = data.get(symbol)
        if not snapshot:
            print(f"{symbol:6s}  — no data returned")
            continue

        latest_trade = snapshot.get("latestTrade", {})
        price = latest_trade.get("p")
        timestamp = latest_trade.get("t")
        print(f"{symbol:6s}  ${price:<10}  {timestamp}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, indent=2))
    print(f"\nWrote raw response to {OUTPUT_PATH}")
