import httpx

from core.config import settings

_BASE_URL = "https://data.alpaca.markets/v2"
_HEADERS = {
    "APCA-API-KEY-ID": settings.alpaca_api_key,
    "APCA-API-SECRET-KEY": settings.alpaca_api_secret,
}

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


def get_symbols() -> list[str]:
    return SYMBOLS


def get_snapshots(symbols: list[str]) -> dict:
    """
    Fetch the latest snapshot for each symbol in a single API call.

    Snapshots include the latest trade price, bid/ask, and daily bar data.
    All symbols are sent as a comma-separated query param so 100 symbols
    cost exactly one request.

    Returns the raw dict keyed by symbol, e.g.:
        {
            "AAPL": { "latestTrade": { "p": 189.50, ... }, ... },
            "MSFT": { ... },
        }
    """
    response = httpx.get(
        f"{_BASE_URL}/stocks/snapshots",
        headers=_HEADERS,
        params={"symbols": ",".join(symbols), "feed": "iex"},
    )
    response.raise_for_status()
    return response.json()


def get_prices(symbols: list[str]) -> dict[str, dict]:
    """
    Returns essential price info for each symbol.

    Example return value:
        {
            "AAPL": {"price": 189.50, "timestamp": "2025-03-09T14:32:00Z"},
            "MSFT": {"price": 412.10, "timestamp": "2025-03-09T14:32:01Z"},
        }

    Symbols with no data are omitted from the result.
    """
    raw = get_snapshots(symbols)
    result = {}
    for symbol, snapshot in raw.items():
        trade = snapshot.get("latestTrade", {})
        price = trade.get("p")
        timestamp = trade.get("t")
        if price is not None and timestamp is not None:
            result[symbol] = {"price": price, "timestamp": timestamp, "symbol": symbol}
    return result
