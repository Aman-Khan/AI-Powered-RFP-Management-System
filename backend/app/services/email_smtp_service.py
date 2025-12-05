from email.message import EmailMessage
import aiosmtplib
from fastapi import HTTPException
from app.core.config import settings

async def send_email_smtp(to_emails: list[str], subject: str, content: str):
    msg = EmailMessage()
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject

    # Convert line breaks to HTML
    html_content = content.replace("\n", "<br/>")

    msg.set_content(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            start_tls=True,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASS
        )

        return {"status": "sent", "recipients": to_emails}

    except Exception as e:
        print("SMTP ERROR:", e)
        raise HTTPException(status_code=500, detail="SMTP sending failed")
