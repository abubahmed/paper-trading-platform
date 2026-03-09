from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.account import Account
from models.balance import Balance
from models.competition import Competition
from models.position import Position
from models.price import Price
from models.user import User
from schemas.leaderboard import LeaderboardEntryResponse

router = APIRouter()


@router.get("/", response_model=list[LeaderboardEntryResponse])
def get_leaderboard(db: Session = Depends(get_db)):
    """
    Return ranked leaderboard standings for the active competition.

    Each entry shows the user's total portfolio value (cash + market value of
    all positions), sorted from highest to lowest. total_value and positions_value
    are null if price data is missing for any symbol that user holds. No
    authentication required.
    """
    competition = db.query(Competition).filter(Competition.is_active == True).first()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active competition")

    accounts = db.query(Account).filter(Account.competition_id == competition.id).all()

    # Fetch all prices in one query
    all_prices = {row.symbol: Decimal(str(row.price)) for row in db.query(Price).all()}

    entries = []
    for account in accounts:
        user = db.query(User).filter(User.id == account.user_id).first()
        balance = db.query(Balance).filter(Balance.account_id == account.id).first()
        positions = db.query(Position).filter(Position.account_id == account.id).all()

        if not balance:
            continue

        cash = Decimal(str(balance.available_amount)) + Decimal(str(balance.reserved_amount))

        positions_value: Decimal | None = Decimal("0")
        for pos in positions:
            price = all_prices.get(pos.symbol)
            if price is None:
                positions_value = None
                break
            positions_value += price * pos.quantity  # type: ignore[operator]

        total_value = (cash + positions_value) if positions_value is not None else None

        entries.append(
            LeaderboardEntryResponse(
                rank=0,  # assigned after sorting
                username=user.username,
                total_value=total_value,
                cash=cash,
                positions_value=positions_value,
            )
        )

    # Sort: users with a total_value rank highest, null total_values go to the bottom
    entries.sort(key=lambda e: (e.total_value is None, -(e.total_value or 0)))

    for i, entry in enumerate(entries, start=1):
        entry.rank = i

    return entries
