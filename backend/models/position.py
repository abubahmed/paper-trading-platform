import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Position(Base):
    """
    Tracks how many shares of a given stock an Account holds.

    One Position row exists per (account, symbol) pair. Like Balance, shares are
    split into available and reserved buckets. When a sell order is placed, shares
    move from quantity to reserved_quantity to prevent overselling. When the sell
    fills, reserved_quantity is decremented. When it cancels, shares return to quantity.

    Attributes:
        id:                Primary key (UUID).
        account_id:        Foreign key to the Account holding this position.
        symbol:            Ticker symbol of the held stock (e.g. "AAPL").
        quantity:          Shares available to sell or count toward portfolio value.
        reserved_quantity: Shares locked against pending open sell orders.
        updated_at:        Timestamp of the last modification by the trading engine.
        account:           The Account this position belongs to.
    """

    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("account_id", "symbol"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="positions")
