"""
ingest_prices.py — Price ingestion job.

Fetches the latest market prices for all tracked symbols from Alpaca,
upserts them into the prices table, then publishes a PRICE_UPDATE message
to Redis so the trading engine knows to re-evaluate open limit orders.

Intended to be run on a fixed schedule (e.g. every 3 minutes). Each run
is a single shot — scheduling is handled externally.

Usage (from backend/):
    uv run ingest-prices
    python -m scripts.ingest_prices
"""

import json
import logging
from datetime import datetime, timezone

import redis

from core.config import settings
from core.database import SessionLocal
from services.alpaca import get_prices
from services.prices import upsert_prices

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "BRK.B", "JPM", "V",
    "UNH", "XOM", "LLY", "JNJ", "WMT", "MA", "PG", "ORCL", "HD", "AVGO",
    "CVX", "MRK", "KO", "PEP", "ABBV", "COST", "BAC", "MCD", "ADBE", "SPY",
]


def ingest() -> None:
    log.info("Fetching prices for %d symbols", len(SYMBOLS))
    prices = get_prices(SYMBOLS)

    if not prices:
        log.warning("No price data returned — aborting")
        return

    with SessionLocal() as db:
        count = upsert_prices(db, prices)
    log.info("Upserted %d prices into the database", count)

    r = redis.from_url(settings.redis_url)
    message = json.dumps({
        "type": "PRICE_UPDATE",
        "symbols": list(prices.keys()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    r.lpush("trading_engine", message)
    log.info("Published PRICE_UPDATE to Redis for %d symbols", len(prices))


if __name__ == "__main__":
    ingest()
