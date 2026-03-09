from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.price import Price
from schemas.prices import PriceResponse

router = APIRouter()


@router.get("/", response_model=list[PriceResponse])
def get_prices(db: Session = Depends(get_db)):
    """
    Return the latest cached market price for every tracked symbol.

    Prices are written by the price ingestion job every 3 minutes using data
    from the Alpaca API. This endpoint requires no authentication — it reflects
    the same prices the trading engine uses when evaluating and executing orders.
    """
    return db.query(Price).order_by(Price.symbol).all()
