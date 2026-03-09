from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PriceResponse(BaseModel):
    symbol: str
    price: Decimal
    updated_at: datetime

    model_config = {"from_attributes": True}
