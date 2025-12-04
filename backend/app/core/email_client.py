import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

sg = SendGridAPIClient(settings.SENDGRID_KEY)

async def send_email(to, subject, html):
    message = Mail(
        from_email=settings.EMAIL_FROM,
        to_emails=to,
        subject=subject,
        html_content=html,
    )
    return sg.send(message)
