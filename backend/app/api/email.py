from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.prisma import prisma
from app.services.email_smtp_service import send_email_smtp
from app.utils.ids import new_id

router = APIRouter(tags=["Email Management"])

class SendEmailRequest(BaseModel):
    rfpId: str
    vendorIds: list[str]
    subject: str
    content: str


@router.post("/send")
async def send_email(payload: SendEmailRequest):
    """
    Sends an email to a list of vendors for a specific RFP,
    creates RFPVendor records, and logs the outgoing emails.
    """
    sent_count = 0

    for vendor_id in payload.vendorIds:

        vendor = await prisma.vendor.find_unique(where={"id": vendor_id})
        
        if not vendor or not vendor.email:
            print(f"Skipping vendor {vendor_id}: not found or missing email.")
            continue

        personalized = payload.content.replace("{vendor_name}", vendor.name)

        html_body = personalized.replace("\n", "<br/>")
        
        now_utc = datetime.now(timezone.utc)

        try:
            rfp_vendor = await prisma.rfpvendor.create(
                data={
                    "rfpId": payload.rfpId,
                    "vendorId": vendor_id,
                    "status": "sent",
                    "sentAt": now_utc
                }
            )
        except Exception as e:
            print(f"Error creating RFPVendor for vendor {vendor_id}: {e}")
            continue

        try:
            print(html_body)
            await send_email_smtp(
                to_emails=[vendor.email],
                subject=payload.subject,
                content=html_body
            )
        except Exception as e:
            print(f"Error sending email to {vendor.email}: {e}")
            continue

        try:
            await prisma.emaillog.create(
                data={
                    "rfpVendorId": rfp_vendor.id,
                    "direction": "outgoing",
                    "subject": payload.subject,
                    "body": html_body
                }
            )
        except Exception as e:
            print(f"Error logging email for RFPVendor {rfp_vendor.id}: {e}")

        sent_count += 1

    return {
        "status": "ok",
        "count": sent_count
    }