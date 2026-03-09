"""
test_alpaca.py — Sanity check for the Alpaca snapshot client.

Fetches the latest price snapshot for 10 common symbols and prints a
clean summary. Useful for verifying API credentials and inspecting the
raw response shape before building the ingestion job.

Usage (from backend/):
    python -m scripts.test_alpaca
"""

import json
from services.alpaca import get_snapshots

SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "V", "SPY"]


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

    print("\n--- raw response ---")
    print(json.dumps(data, indent=2))
