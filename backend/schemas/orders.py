import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator, model_validator

from models.order import OrderSide, OrderStatus, OrderType


class CreateOrderRequest(BaseModel):
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: int
    limit_price: Decimal | None = None

    @field_validator("symbol")
    @classmethod
    def symbol_upper(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("quantity must be greater than zero")
        return v

    @model_validator(mode="after")
    def limit_price_required_for_limit_orders(self) -> "CreateOrderRequest":
        if self.type == OrderType.LIMIT and self.limit_price is None:
            raise ValueError("limit_price is required for LIMIT orders")
        if self.type == OrderType.MARKET and self.limit_price is not None:
            raise ValueError("limit_price must not be set for MARKET orders")
        return self


class CancelOrderRequest(BaseModel):
    order_id: uuid.UUID


class TradeResponse(BaseModel):
    id: uuid.UUID
    symbol: str
    side: OrderSide
    quantity: int
    price: Decimal
    executed_at: datetime

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: int
    status: OrderStatus
    limit_price: Decimal | None
    filled_at: datetime | None
    canceled_at: datetime | None
    created_at: datetime
    trade: TradeResponse | None = None

    model_config = {"from_attributes": True}
