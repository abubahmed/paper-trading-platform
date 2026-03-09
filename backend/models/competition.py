import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Competition(Base):
    """
    Represents a single trading competition season.

    Each competition has a fixed time window and starting cash amount. Only one
    competition can be active at a time. When a competition ends, all open orders
    are automatically cancelled and final leaderboard rankings are locked.

    Attributes:
        id:           Primary key (UUID).
        name:         Display name for the competition (e.g. "Spring 2025").
        description:  Optional longer description shown to students.
        start_time:   When the competition opens and trading begins.
        end_time:     When the competition closes and trading stops.
        initial_cash: Starting cash balance issued to every participant.
        is_active:    Whether this is the currently running competition; only one can be True at a time.
        created_at:   Timestamp when the competition was created by an admin.
        accounts:     All participant accounts enrolled in this competition.
        orders:       All orders placed within this competition.
    """

    __tablename__ = "competitions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    initial_cash: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="competition")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="competition")
