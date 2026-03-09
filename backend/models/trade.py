import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from models.order import OrderSide


class Trade(Base):
    """
    Represents a successfully executed transaction.

    A Trade is created by the trading engine only when an Order is actually
    filled. It is the immutable ledger record of what happened — what was
    bought or sold, at what price, and when. Every Trade corresponds to
    exactly one Order.

    Attributes:
        id:          Primary key (UUID).
        order_id:    Foreign key to the Order that triggered this trade.
        account_id:  Foreign key to the Account that owns this trade.
        symbol:      Ticker symbol that was traded (e.g. "AAPL").
        side:        Direction of the trade — BUY or SELL.
        quantity:    Number of shares that were executed.
        price:       Price per share at the time of execution.
        executed_at: Timestamp when the trade was executed by the trading engine.
        order:       The Order that was filled to produce this trade.
        account:     The Account this trade belongs to.
    """

    __tablename__ = "trades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    side: Mapped[OrderSide] = mapped_column(Enum(OrderSide), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="trade")
    account: Mapped["Account"] = relationship("Account", back_populates="trades")
