import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class User(Base):
    """
    Represents a Princeton student registered on the platform.

    A User is created automatically on first Clerk login and is scoped to a
    Princeton email. A single User can participate in multiple competitions,
    each participation represented by a separate Account.

    Attributes:
        id:           Primary key (UUID).
        clerk_id:     Unique identifier issued by Clerk after SSO login.
        first_name:   Student's first name.
        last_name:    Student's last name.
        email:        Princeton email address (unique).
        username:     Chosen display name (unique).
        netid:        Princeton NetID (unique).
        class_year:   Graduation year (optional).
        active:       Whether the account is in good standing; admins can set False to ban.
        last_seen_at: Timestamp of the user's most recent authenticated request.
        created_at:   Timestamp when the user record was first created.
        accounts:     All competition accounts belonging to this user.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    netid: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    class_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="user")
