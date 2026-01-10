"""Interfaces for external services."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

class IEmailService(ABC):
    """Interface for email notifications."""
    
    @abstractmethod
    async def send_welcome_email(self, email: str, full_name: str):
        """Send a welcome email to a new user."""
        pass

    @abstractmethod
    async def send_performance_alert(self, email: str, database_name: str, issue_title: str, query_fingerprint: str):
        """Send an alert about a performance regression."""
        pass

class IBillingService(ABC):
    """Interface for billing and subscriptions."""
    
    @abstractmethod
    async def create_customer(self, email: str, name: str) -> str:
        """Create a customer in the payment gateway."""
        pass

    @abstractmethod
    async def create_checkout_session(self, customer_id: str, plan_price_id: str, success_url: str, cancel_url: str) -> str:
        """Create a checkout session and return the URL."""
        pass

    @abstractmethod
    async def create_portal_session(self, customer_id: str, return_url: str) -> str:
        """Create a self-service billing portal session."""
        pass
