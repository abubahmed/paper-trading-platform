import uuid
from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: uuid.UUID
    clerk_id: str
    first_name: str
    last_name: str
    email: str
    username: str
    netid: str
    class_year: int | None
    active: bool
    last_seen_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
