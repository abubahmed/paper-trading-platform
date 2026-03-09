from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.account import Account
from models.balance import Balance
from models.competition import Competition
from models.position import Position
from models.price import Price
from models.user import User
from schemas.portfolio import (
    BalanceResponse,
    PortfolioSummaryResponse,
    PortfolioValueResponse,
    PositionResponse,
)


def _get_active_competition(db: Session) -> Competition:
    competition = db.query(Competition).filter(Competition.is_active == True).first()
    if not competition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active competition")
    return competition


def _get_account(db: Session, user: User, competition: Competition) -> Account:
    account = (
        db.query(Account)
        .filter(Account.user_id == user.id, Account.competition_id == competition.id)
        .first()
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not enrolled in the active competition",
        )
    return account


def get_balance(db: Session, user: User) -> BalanceResponse:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    balance = db.query(Balance).filter(Balance.account_id == account.id).first()
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found")

    return BalanceResponse(
        available=balance.available_amount,
        reserved=balance.reserved_amount,
        total=Decimal(str(balance.available_amount)) + Decimal(str(balance.reserved_amount)),
        updated_at=balance.updated_at,
    )


def get_positions(db: Session, user: User) -> list[PositionResponse]:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    positions = db.query(Position).filter(Position.account_id == account.id).all()

    # Fetch prices for all held symbols in one query
    symbols = [p.symbol for p in positions]
    prices = {
        row.symbol: row.price
        for row in db.query(Price).filter(Price.symbol.in_(symbols)).all()
    }

    result = []
    for pos in positions:
        price = prices.get(pos.symbol)
        market_value = (
            Decimal(str(price)) * pos.quantity if price is not None else None
        )
        result.append(PositionResponse(
            symbol=pos.symbol,
            quantity=pos.quantity,
            reserved_quantity=pos.reserved_quantity,
            current_price=Decimal(str(price)) if price is not None else None,
            market_value=market_value,
            updated_at=pos.updated_at,
        ))

    return result


def get_portfolio_value(db: Session, user: User) -> PortfolioValueResponse:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    balance = db.query(Balance).filter(Balance.account_id == account.id).first()
    if not balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Balance not found")

    cash = Decimal(str(balance.available_amount)) + Decimal(str(balance.reserved_amount))

    positions = db.query(Position).filter(Position.account_id == account.id).all()
    symbols = [p.symbol for p in positions]
    prices = {
        row.symbol: row.price
        for row in db.query(Price).filter(Price.symbol.in_(symbols)).all()
    }

    positions_value: Decimal | None = Decimal("0")
    for pos in positions:
        price = prices.get(pos.symbol)
        if price is None:
            positions_value = None
            break
        positions_value += Decimal(str(price)) * pos.quantity  # type: ignore[operator]

    total_value = (cash + positions_value) if positions_value is not None else None

    return PortfolioValueResponse(
        cash=cash,
        positions_value=positions_value,
        total_value=total_value,
    )


def get_portfolio_summary(db: Session, user: User) -> PortfolioSummaryResponse:
    return PortfolioSummaryResponse(
        balance=get_balance(db, user),
        positions=get_positions(db, user),
        value=get_portfolio_value(db, user),
    )
