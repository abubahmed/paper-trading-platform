import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.queue import enqueue_order
from models.account import Account
from models.competition import Competition
from models.order import Order, OrderStatus
from models.user import User
from schemas.orders import CancelOrderRequest, CreateOrderRequest


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


def create_order(db: Session, user: User, data: CreateOrderRequest) -> Order:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    order = Order(
        account_id=account.id,
        competition_id=competition.id,
        symbol=data.symbol,
        side=data.side,
        type=data.type,
        quantity=data.quantity,
        limit_price=data.limit_price,
        status=OrderStatus.OPEN,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    enqueue_order(str(order.id))
    return order


def cancel_order(db: Session, user: User, data: CancelOrderRequest) -> Order:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    order = (
        db.query(Order)
        .filter(Order.id == data.order_id, Order.account_id == account.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.status != OrderStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Order cannot be cancelled (status: {order.status})",
        )

    order.status = OrderStatus.CANCELED
    order.canceled_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, user: User) -> list[Order]:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    return (
        db.query(Order)
        .filter(Order.account_id == account.id)
        .order_by(Order.created_at.desc())
        .all()
    )


def list_open_orders(db: Session, user: User) -> list[Order]:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    return (
        db.query(Order)
        .filter(Order.account_id == account.id, Order.status == OrderStatus.OPEN)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order(db: Session, user: User, order_id: uuid.UUID) -> Order:
    competition = _get_active_competition(db)
    account = _get_account(db, user, competition)

    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.account_id == account.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
