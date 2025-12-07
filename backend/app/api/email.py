from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.db_client import prisma
from app.services.email_smtp_service import send_email_smtp
from app.services.email_imap_service import fetch_incoming_emails
from app.utils.email_parser import extract_tracking_id
from app.utils.ids import new_id
import time
from prisma import Json
from app.tasks.email_sync import sync_replies_once

uid = int(time.time() * 1000)
router = APIRouter(tags=["Email Management"])

class SendEmailRequest(BaseModel):
    rfpId: str
    vendorIds: list[str]
    subject: str
    content: str


@router.post("/send")
async def send_email(payload: SendEmailRequest):

    sent_count = 0

    for vendor_id in payload.vendorIds:

        vendor = await prisma.vendor.find_unique(where={"id": vendor_id})
        if not vendor or not vendor.email:
            print(f"Skipping vendor {vendor_id}")
            continue

        # personalize body
        personalized_text = payload.content.replace("{vendor_name}", vendor.name)
        html_body = personalized_text.replace("\n", "<br/>")

        # Create RFPVendor first (so we get ID)
        now_utc = datetime.now(timezone.utc)

        rfp_vendor = await prisma.rfpvendor.create(
            data={
                "id": new_id(),
                "rfpId": payload.rfpId,
                "vendorId": vendor_id,
                "status": "sent",
                "sentAt": now_utc
            }
        )

        # append Ref-ID for tracking replies
        tracking_html = html_body + f"<br/><br/><small>Ref-ID:{rfp_vendor.id}</small>"

        # send email
        await send_email_smtp(
            to_emails=[vendor.email],
            subject=payload.subject,
            content=tracking_html
        )

        # log outgoing email — UID intentionally None (incoming only)
        await prisma.emaillog.create(
            data={
                "id": new_id(),
                "uid": int(time.time() * 1000),     # 🔥 Temporary placeholder (required by schema)
                "rfpVendorId": rfp_vendor.id,
                "direction": "outgoing",
                "subject": payload.subject,
                "body": tracking_html
            }
        )

        sent_count += 1

    return {"status": "ok", "count": sent_count}


@router.get("/receive")
async def receive_and_map_emails():
    """Manual trigger of email sync."""
    return await sync_replies_once()

# async def receive_and_map_emails():

#     emails = fetch_incoming_emails(include_seen=True, hours=2)

#     saved = 0
#     skipped = 0
#     duplicates = 0

#     for mail in emails:

#         uid = int(mail["msgId"])
#         body = mail["body"] or ""

#         # Duplicate check
#         existing = await prisma.emaillog.find_unique(where={"uid": uid})
#         if existing:
#             duplicates += 1
#             continue

#         # Extract tracking ID
#         tracking_id = extract_tracking_id(body)
#         if not tracking_id:
#             skipped += 1
#             continue

#         rfp_vendor = await prisma.rfpvendor.find_unique(where={"id": tracking_id})
#         if not rfp_vendor:
#             skipped += 1
#             continue

#         print("📩 Saving EmailLog:")
#         print("  msgId:", uid)
#         print("  vendor:", tracking_id)
#         print("  subject:", mail["subject"])
#         print("  body preview:", body[:120].replace("\n", "\\n"))

#         # Save EmailLog
#         await prisma.emaillog.create(
#             data={
#                 "uid": uid,
#                 "rfpVendorId": tracking_id,
#                 "direction": "incoming",
#                 "subject": mail.get("subject"),
#                 "body": body,
#                 "attachments": Json(mail.get("attachments") or []),
#             }
#         )

#         # Update vendor status
#         await prisma.rfpvendor.update(
#             where={"id": tracking_id},
#             data={"status": "replied"}
#         )

#         saved += 1

#     return {
#         "status": "ok",
#         "received": len(emails),
#         "saved": saved,
#         "skipped": skipped,
#         "duplicates": duplicates
#     }