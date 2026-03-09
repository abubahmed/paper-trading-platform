from decimal import Decimal

from pydantic import BaseModel


class LeaderboardEntryResponse(BaseModel):
    rank: int
    username: str
    total_value: Decimal | None
    cash: Decimal
    positions_value: Decimal | None
