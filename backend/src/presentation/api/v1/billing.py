"""Billing API routes for Stripe integration."""
from typing import Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from src.application.interfaces.services.external_services import IBillingService
from src.infrastructure.services.billing_service import StripeBillingService
from src.infrastructure.database.session import get_db_session
from src.infrastructure.database.repositories.user_repository import PostgresUserRepository
from src.presentation.api.v1.deps import get_current_user
from src.domain.entities.user import User, PlanTier
from src.config import get_settings, Settings

router = APIRouter(prefix="/billing", tags=["billing"])

class CreateCheckoutRequest(BaseModel):
    plan_tier: PlanTier
    success_url: str
    cancel_url: str

@router.post("/checkout")
async def create_checkout_session(
    request: CreateCheckoutRequest,
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
    db = Depends(get_db_session)
):
    """Create a Stripe checkout session for a plan."""
    user_repo = PostgresUserRepository(db)
    billing_service = StripeBillingService(settings)
    
    # 1. Ensure user has a stripe customer ID
    if not current_user.stripe_customer_id:
        customer_id = await billing_service.create_customer(current_user.email, current_user.full_name or "")
        current_user.stripe_customer_id = customer_id
        await user_repo.update(current_user)
    
    # 2. Get price ID for the requested plan
    # In a real app, these would be in settings or a database
    price_ids = {
        PlanTier.STARTER: "price_starter_id",
        PlanTier.PRO: "price_pro_id",
        PlanTier.ENTERPRISE: "price_enterprise_id"
    }
    
    price_id = price_ids.get(request.plan_tier)
    if not price_id:
        raise HTTPException(status_code=400, detail="Invalid plan tier")
        
    # 3. Create checkout session
    checkout_url = await billing_service.create_checkout_session(
        current_user.stripe_customer_id,
        price_id,
        request.success_url,
        request.cancel_url
    )
    
    return {"checkout_url": checkout_url}

@router.post("/portal")
async def create_portal_session(
    return_url: str,
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings)
):
    """Create a Stripe billing portal session."""
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No billing account found")
        
    billing_service = StripeBillingService(settings)
    portal_url = await billing_service.create_portal_session(
        current_user.stripe_customer_id,
        return_url
    )
    
    return {"portal_url": portal_url}

@router.post("/webhook")
async def stripe_webhook(request: Request, settings: Settings = Depends(get_settings)):
    """Handle Stripe webhooks."""
    # This would involve verifying signature and updating user plans
    # Skipping detailed implementation for now as it needs a valid secret
    return {"status": "success"}
