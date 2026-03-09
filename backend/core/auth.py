"""
core/auth.py — Request authentication dependency.

DEV MODE: The Bearer token is treated as the raw clerk_id (e.g. "user_seed_001").
TODO: Replace _resolve_clerk_id with real Clerk JWT verification before production.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User

_bearer = HTTPBearer()


def _resolve_clerk_id(token: str) -> str:
    """Dev stub: token IS the clerk_id. Swap this for real JWT verification later."""
    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    clerk_id = _resolve_clerk_id(credentials.credentials)

    user = db.query(User).filter(User.clerk_id == clerk_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")
    return user
