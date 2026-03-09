from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_db
from models.user import User
from schemas.portfolio import (
    BalanceResponse,
    PortfolioSummaryResponse,
    PortfolioValueResponse,
    PositionResponse,
)
import services.portfolio as portfolio_service

router = APIRouter()


@router.get("/balance", response_model=BalanceResponse)
def get_balance(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Return the authenticated user's cash balance for the active competition.

    Returns available cash (free to spend), reserved cash (held against open
    buy orders), and the combined total.
    """
    return portfolio_service.get_balance(db, user)


@router.get("/positions", response_model=list[PositionResponse])
def get_positions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Return all stock positions held by the authenticated user in the active competition.

    Each position includes the current market price and computed market value
    where price data is available. current_price and market_value are null if
    the price ingestion job has not yet loaded data for that symbol.
    """
    return portfolio_service.get_positions(db, user)


@router.get("/value", response_model=PortfolioValueResponse)
def get_portfolio_value(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Return the total portfolio value for the authenticated user in the active competition.

    Sums cash (available + reserved) with the market value of all positions.
    positions_value and total_value are null if price data is missing for any
    held symbol.
    """
    return portfolio_service.get_portfolio_value(db, user)


@router.get("/summary", response_model=PortfolioSummaryResponse)
def get_portfolio_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Return balance, positions, and portfolio value in a single response.

    Convenience endpoint that combines /balance, /positions, and /value
    to avoid multiple round trips from the frontend.
    """
    return portfolio_service.get_portfolio_summary(db, user)
