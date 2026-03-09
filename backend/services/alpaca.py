import httpx

from core.config import settings

_BASE_URL = "https://data.alpaca.markets/v2"
_HEADERS = {
    "APCA-API-KEY-ID": settings.alpaca_api_key,
    "APCA-API-SECRET-KEY": settings.alpaca_api_secret,
}


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
