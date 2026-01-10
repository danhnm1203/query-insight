from fastapi import APIRouter, Depends
from src.presentation.api.v1.deps import get_current_user
from src.domain.entities.user import User

router = APIRouter(tags=["debug"])

@router.get("/debug-sentry")
async def trigger_error(current_user: User = Depends(get_current_user)):
    """Trigger a division by zero error/exception to test Sentry."""
    return 1 / 0
