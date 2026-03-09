from datetime import datetime, timezone
from sqlalchemy import BigInteger, DateTime, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class Price(Base):
    """
    Stores the latest market price for a tracked stock symbol.

    One row per symbol. The price ingestion job upserts this table every 3
    minutes using data from the Alpaca API. The trading engine reads from this
    table when evaluating and executing orders — it never fetches live prices
    directly.

    Attributes:
        symbol:     Ticker symbol and primary key (e.g. "AAPL").
        price:      Most recent traded price fetched from the market data provider.
        updated_at: Timestamp of the last price update from the ingestion job.
    """

    __tablename__ = "prices"

    symbol: Mapped[str] = mapped_column(String, primary_key=True)
    price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class PriceBar(Base):
    """
    Stores OHLCV candlestick data for a symbol at a specific timeframe.

    Used to power price charts in the frontend and to supply historical price
    data to student trading bots via the on_price_update context. Rows are
    written by the price ingestion job. A unique constraint on (symbol,
    timestamp, timeframe) prevents duplicate bars.

    Attributes:
        id:        Auto-incrementing primary key.
        symbol:    Ticker symbol this bar belongs to (e.g. "AAPL").
        timestamp: Start of the bar's time interval (timezone-aware).
        timeframe: Bar duration (e.g. "1Min", "5Min", "1Day").
        open:      Price at the start of the interval.
        high:      Highest price during the interval.
        low:       Lowest price during the interval.
        close:     Price at the end of the interval.
        volume:    Number of shares traded during the interval.
    """

    __tablename__ = "price_bars"
    __table_args__ = (UniqueConstraint("symbol", "timestamp", "timeframe"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timeframe: Mapped[str] = mapped_column(String, nullable=False)
    open: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    high: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    low: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    close: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
