import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class OrderSide(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderStatus(str, enum.Enum):
    OPEN = "OPEN"
    FILLED = "FILLED"
    CANCELED = "CANCELED"


class Order(Base):
    """
    Represents a student's intent to buy or sell a stock.

    An Order is a request, not a guarantee of execution. Market orders execute
    immediately at the current cached price. Limit orders sit OPEN until the
    market price meets the limit condition, at which point the trading engine
    fills them on the next price update cycle. Orders that are still OPEN when
    a competition ends are automatically cancelled.

    Attributes:
        id:             Primary key (UUID).
        account_id:     Foreign key to the Account that placed the order.
        competition_id: Foreign key to the Competition this order belongs to.
        symbol:         Ticker symbol being traded (e.g. "AAPL").
        side:           Direction of the trade — BUY or SELL.
        type:           Order type — MARKET (execute now) or LIMIT (execute at price).
        quantity:       Number of shares to buy or sell.
        status:         Current state — OPEN, FILLED, or CANCELED.
        limit_price:    Target execution price; only set for LIMIT orders.
        filled_at:      Timestamp when the order was executed; null if not yet filled.
        canceled_at:    Timestamp when the order was cancelled; null if not cancelled.
        created_at:     Timestamp when the order was submitted.
        account:        The Account that placed this order.
        competition:    The Competition this order is scoped to.
        trade:          The resulting Trade record if the order was filled.
    """

    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    competition_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competitions.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    side: Mapped[OrderSide] = mapped_column(Enum(OrderSide), nullable=False)
    type: Mapped[OrderType] = mapped_column(Enum(OrderType), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.OPEN, nullable=False)
    limit_price: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    filled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    canceled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="orders")
    competition: Mapped["Competition"] = relationship("Competition", back_populates="orders")
    trade: Mapped["Trade | None"] = relationship("Trade", back_populates="order", uselist=False)
