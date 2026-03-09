from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BalanceResponse(BaseModel):
    available: Decimal
    reserved: Decimal
    total: Decimal
    updated_at: datetime

    model_config = {"from_attributes": True}


class PositionResponse(BaseModel):
    symbol: str
    quantity: int
    reserved_quantity: int
    current_price: Decimal | None  # null if no price data exists yet
    market_value: Decimal | None   # null if no price data exists yet
    updated_at: datetime

    model_config = {"from_attributes": True}


class PortfolioValueResponse(BaseModel):
    cash: Decimal                        # available + reserved
    positions_value: Decimal | None      # null if any position is missing a price
    total_value: Decimal | None          # cash + positions_value; null if positions_value is null


class PortfolioSummaryResponse(BaseModel):
    balance: BalanceResponse
    positions: list[PositionResponse]
    value: PortfolioValueResponse
