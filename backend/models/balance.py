import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Balance(Base):
    """
    Tracks the cash balance for an Account within a competition.

    Each Account has exactly one Balance record. Cash is split into two buckets:
    available (free to spend) and reserved (held against open buy orders). When
    a buy order is placed, cash moves from available to reserved. When it fills,
    reserved is decremented. When it cancels, reserved is returned to available.

    Attributes:
        id:               Primary key (UUID).
        account_id:       Foreign key to the Account this balance belongs to (unique).
        available_amount: Cash the student can freely use for new orders.
        reserved_amount:  Cash locked against pending open buy orders.
        updated_at:       Timestamp of the last modification by the trading engine.
        account:          The Account this balance belongs to.
    """

    __tablename__ = "balances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), unique=True, nullable=False)
    available_amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    reserved_amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="balance")
