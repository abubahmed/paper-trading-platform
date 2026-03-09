import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Account(Base):
    """
    Represents a user's participation in a specific competition.

    An Account is the join entity between a User and a Competition. It acts as
    the owner of all trading activity within that competition — orders, trades,
    balances, and positions all belong to an Account rather than directly to a
    User. A user gets exactly one Account per competition.

    Attributes:
        id:             Primary key (UUID).
        user_id:        Foreign key to the User who owns this account.
        competition_id: Foreign key to the Competition this account belongs to.
        created_at:     Timestamp when the account was created (i.e. user enrolled).
        user:           The User this account belongs to.
        competition:    The Competition this account is enrolled in.
        orders:         All orders placed by this account.
        trades:         All executed trades for this account.
        balance:        The single cash balance record for this account.
        positions:      All open stock positions held by this account.
    """

    __tablename__ = "accounts"
    __table_args__ = (UniqueConstraint("user_id", "competition_id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    competition_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competitions.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="accounts")
    competition: Mapped["Competition"] = relationship("Competition", back_populates="accounts")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="account")
    trades: Mapped[list["Trade"]] = relationship("Trade", back_populates="account")
    balance: Mapped["Balance"] = relationship("Balance", back_populates="account", uselist=False)
    positions: Mapped[list["Position"]] = relationship("Position", back_populates="account")
