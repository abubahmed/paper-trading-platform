from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.price import Price


def get_price(db: Session, symbol: str) -> Price:
    """Return the latest cached price row for a symbol, or 404 if not found."""
    price = db.query(Price).filter(Price.symbol == symbol).first()
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No price data for symbol '{symbol}'",
        )
    return price


def get_all_prices(db: Session) -> list[Price]:
    """Return cached price rows for all tracked symbols."""
    return db.query(Price).order_by(Price.symbol).all()


def upsert_prices(db: Session, prices: dict[str, dict]) -> int:
    """
    Bulk-upsert price data into the prices table.

    Expects the dict returned by services.alpaca.get_prices():
        { "AAPL": {"price": 189.50, "timestamp": "...", "symbol": "AAPL"}, ... }

    Inserts new rows and updates price + updated_at for existing ones.
    Returns the number of rows written.
    """
    if not prices:
        return 0

    now = datetime.now(timezone.utc)
    rows = [{"symbol": symbol, "price": data["price"], "updated_at": now} for symbol, data in prices.items()]

    stmt = insert(Price).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["symbol"],
        set_={
            "price": stmt.excluded.price,
            "updated_at": stmt.excluded.updated_at,
        },
    )
    db.execute(stmt)
    db.commit()

    return len(rows)
