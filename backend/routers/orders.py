import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_db
from models.user import User
from schemas.orders import (
    CancelOrderRequest,
    CreateOrderRequest,
    OrderResponse,
)
import services.orders as order_service

router = APIRouter()


@router.post("/create", response_model=OrderResponse, status_code=201)
def create_order(
    body: CreateOrderRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Submit a new order for the active competition.

    Accepts a symbol, side (BUY/SELL), type (MARKET/LIMIT), quantity, and
    an optional limit_price (required for LIMIT orders). Returns the persisted
    order with status OPEN.
    """
    return order_service.create_order(db, user, body)


@router.post("/cancel", response_model=OrderResponse)
def cancel_order(
    body: CancelOrderRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Cancel an open order.

    Accepts an order_id. The order must belong to the authenticated user and
    be in OPEN status. Returns the updated order with status CANCELED.
    """
    return order_service.cancel_order(db, user, body)


@router.get("/list", response_model=list[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    List all orders for the authenticated user in the active competition.

    Returns all orders regardless of status, sorted newest first.
    """
    return order_service.list_orders(db, user)


@router.get("/open", response_model=list[OrderResponse])
def list_open_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    List all open orders for the authenticated user in the active competition.

    Returns only orders with status OPEN, sorted newest first.
    """
    return order_service.list_open_orders(db, user)


@router.get("/get", response_model=OrderResponse)
def get_order(
    order_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get a single order by ID.

    Accepts order_id as a query parameter. Returns full order detail including
    trade execution info if the order has been filled. Scoped to the authenticated
    user and active competition.
    """
    return order_service.get_order(db, user, order_id)
