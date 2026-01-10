"""User entity for authentication and authorization."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class PlanTier(str, Enum):
    """Subscription plan tiers."""
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class User:
    """User entity representing a registered user."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        plan_tier: PlanTier = PlanTier.FREE,
        stripe_customer_id: Optional[str] = None,
        onboarding_completed: bool = False,
        is_active: bool = True,
        user_id: Optional[UUID] = None,
    ):
        self.id = user_id or uuid4()
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.plan_tier = plan_tier
        self.stripe_customer_id = stripe_customer_id
        self.onboarding_completed = onboarding_completed
        self.is_active = is_active
        self.created_at = datetime.utcnow()
        self.last_login_at: Optional[datetime] = None
    
    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login_at = datetime.utcnow()
    
    def upgrade_plan(self, new_plan: PlanTier) -> None:
        """Upgrade user's subscription plan."""
        self.plan_tier = new_plan
    
    def can_add_database(self, current_count: int) -> bool:
        """Check if user can add more databases based on plan."""
        limits = {
            PlanTier.FREE: 1,
            PlanTier.STARTER: 3,
            PlanTier.PRO: 10,
            PlanTier.ENTERPRISE: float('inf'),
        }
        return current_count < limits[self.plan_tier]
    
    def __repr__(self) -> str:
        return f"<User {self.email} ({self.plan_tier})>"
