"""Stripe implementation of billing service."""
import stripe
from typing import Optional

from src.application.interfaces.services.external_services import IBillingService
from src.config import Settings

class StripeBillingService(IBillingService):
    """Stripe implementation of IBillingService."""

    def __init__(self, settings: Settings):
        self.settings = settings
        stripe.api_key = settings.stripe_secret_key

    async def create_customer(self, email: str, name: str) -> str:
        """Create a customer in Stripe."""
        customer = stripe.Customer.create(
            email=email,
            name=name,
            description="QueryInsight Customer"
        )
        return customer.id

    async def create_checkout_session(self, customer_id: str, plan_price_id: str, success_url: str, cancel_url: str) -> str:
        """Create a Stripe checkout session."""
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[
                {
                    "price": plan_price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url

    async def create_portal_session(self, customer_id: str, return_url: str) -> str:
        """Create a Stripe billing portal session."""
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return session.url
