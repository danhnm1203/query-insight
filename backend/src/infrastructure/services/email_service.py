"""Resend implementation of email service."""
import resend
from src.application.interfaces.services.external_services import IEmailService
from src.config import Settings

class ResendEmailService(IEmailService):
    """Resend implementation of IEmailService."""

    def __init__(self, settings: Settings):
        self.settings = settings
        resend.api_key = settings.resend_api_key

    async def send_welcome_email(self, email: str, full_name: str):
        """Send a welcome email to a new user."""
        try:
            resend.Emails.send({
                "from": self.settings.from_email,
                "to": email,
                "subject": "Welcome to QueryInsight!",
                "html": f"""
                <h1>Welcome to QueryInsight, {full_name}!</h1>
                <p>We're excited to have you on board. Start by connecting your first database to begin analyzing your query performance.</p>
                <a href="https://queryinsight.com/databases">Connect your database</a>
                """
            })
        except Exception as e:
            # In a real app, we might want to log this but not fail the registration flow
            print(f"Failed to send welcome email: {e}")

    async def send_performance_alert(self, email: str, database_name: str, issue_title: str, query_fingerprint: str):
        """Send an alert about a performance regression."""
        try:
            resend.Emails.send({
                "from": self.settings.from_email,
                "to": email,
                "subject": f"⚠️ Performance Alert: {database_name}",
                "html": f"""
                <h2>Significant regression detected</h2>
                <p>A performance regression was detected in database: <strong>{database_name}</strong></p>
                <p><strong>Issue:</strong> {issue_title}</p>
                <p><strong>Query Pattern:</strong> <code>{query_fingerprint}</code></p>
                <p>View the details and recommendations on your dashboard:</p>
                <a href="https://queryinsight.com/dashboard">Go to Dashboard</a>
                """
            })
        except Exception as e:
            print(f"Failed to send performance alert: {e}")
