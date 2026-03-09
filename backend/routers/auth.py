from fastapi import APIRouter, Depends

from core.auth import get_current_user
from models.user import User
from schemas.users import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    """
    Return the authenticated user's profile.

    Resolves the Bearer token to a backend user record and returns all
    stored profile fields for that user.
    """
    return user
