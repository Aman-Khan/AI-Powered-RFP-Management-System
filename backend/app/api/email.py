from fastapi import APIRouter
from app.services.email_imap_service import fetch_incoming_emails
from app.services.email_smtp_service import send_email_smtp
from pydantic import BaseModel

router = APIRouter(tags=["Email Management"])

class SendEmailRequest(BaseModel):
    to_emails: list[str]
    subject: str
    content: str

@router.post("/send")
async def send_email(payload: SendEmailRequest):
    return await send_email_smtp(
        to_emails=payload.to_emails,
        subject=payload.subject,
        content=payload.content
    )

@router.get("/received")
def get_received_emails():
    return fetch_incoming_emails()
