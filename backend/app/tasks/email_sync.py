# app/services/email_sync.py (Revised portion of sync_replies_once)
import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from prisma import Json
from html.parser import HTMLParser
import re

from app.services.email_imap_service import fetch_incoming_emails
from app.utils.email_parser import extract_tracking_id
from app.core.db_client import prisma
from app.core.llm.factory import get_llm
from app.services.proposal_processor import process_email_and_attachments

logger = logging.getLogger(__name__)

# --- HTML Cleaning Utility (kept for context) ---

class HTMLTextExtractor(HTMLParser):
    """Simple parser to strip HTML tags and extract clean text."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.ignore_tags = ['style', 'script']
        self.in_ignore = False

    def handle_starttag(self, tag, attrs):
        if tag in self.ignore_tags:
            self.in_ignore = True

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            self.in_ignore = False
        if tag in ['div', 'p', 'br', 'li']:
            self.text.append('\n')

    def handle_data(self, data):
        if not self.in_ignore:
            self.text.append(data)

    def get_text(self):
        return re.sub(r'\s{2,}', ' ', ''.join(self.text).strip())

def _clean_html_body_to_text(html_content: str) -> str:
    """Strips HTML tags to get clean plain text content."""
    if not ("<" in html_content and ">" in html_content):
        return html_content

    try:
        extractor = HTMLTextExtractor()
        extractor.feed(html_content)
        return extractor.get_text()
    except Exception:
        logger.warning("HTML stripping failed. Using raw content.")
        return html_content


# --- Core Synchronization Function (with changes) ---

async def sync_replies_once() -> Dict[str, Union[str, int]]:
    """
    Sync incoming emails, check for replies, save logs, and extract proposals.
    """
    logger.info("Starting email sync.")

    emails: List[Dict[str, Any]] = fetch_incoming_emails(include_seen=True, hours=5)

    logger.info(f"Total fetched emails: {len(emails)}")

    saved: int = 0
    skipped: int = 0
    duplicates: int = 0
    proposals: int = 0

    for mail in emails:
        uid: int = mail.get("msgId", 0)
        body: str = mail.get("body", "")
        subject: str = mail.get("subject", "")
        attachments: List[str] = mail.get("attachments", [])
        
        preview = body[:150].replace("\n", " ").replace("\r", " ")
        logger.info(f"Processing new email (UID: {uid}, Subject: {subject}, Attachments: {len(attachments)})")
        logger.debug(f"Body preview: {preview}")

        # 1️⃣ Duplicate check
        exists = await prisma.emaillog.find_unique(where={"uid": uid})
        
        if exists:
            logger.info(f"Skipped email {uid}: duplicate UID found.")
            duplicates += 1
            continue

        # 2️⃣ Clean Body and Extract Ref-ID
        # 🔥 CRITICAL CHANGE: Clean the body here.
        clean_body: str = _clean_html_body_to_text(body) 
        
        tracking_id: Optional[str] = extract_tracking_id(clean_body)
        logger.debug(f"Extracted Ref-ID: {tracking_id}")

        if not tracking_id:
            logger.warning(f"No Ref-ID found for email {uid}. Skipping.")
            skipped += 1
            continue

        rfp_vendor = await prisma.rfpvendor.find_unique(where={"id": tracking_id})

        if not rfp_vendor:
            logger.warning(f"No matching RFPVendor found for Ref-ID {tracking_id}. Skipping email {uid}.")
            skipped += 1
            continue
            
        logger.info(f"Found matching vendor {tracking_id}.")

        # 3️⃣ Save Email Log
        try:
            # 🔥 FIX APPLIED: Saving clean_body instead of the original raw body.
            await prisma.emaillog.create(
                data={
                    "uid": uid,
                    "rfpVendorId": tracking_id,
                    "direction": "incoming",
                    "subject": subject,
                    "body": clean_body, # <--- 🌟 SAVING CLEAN TEXT HERE
                    "attachments": Json(attachments),
                }
            )
            logger.info("EmailLog saved successfully with clean body.")
            saved += 1

        except Exception:
            logger.exception("Error saving EmailLog to DB.")
            continue

        # 4️⃣ Update vendor status (omitted for brevity, no change needed)
        try:
            await prisma.rfpvendor.update(
                where={"id": tracking_id},
                data={"status": "replied"}
            )
            logger.info(f"Vendor status updated to 'replied' for {tracking_id}.")
        except Exception:
            logger.exception(f"Error updating vendor status for {tracking_id}.")

        # 5️⃣ & 6️⃣ Proposal extraction
        try:
            logger.info("Running proposal extraction...")
            # Using clean_body for processing
            structured = process_email_and_attachments(clean_body, attachments) 

            # if structured and structured.get('error'):
            #     logger.warning(f"Proposal extraction failed for {tracking_id}. Error: {structured.get('error')}")
            #     continue
                
            logger.debug(f"Extracted structured JSON: {structured}")

        except Exception:
            logger.exception("Proposal extraction failed unexpectedly.")
            continue

        # 7️⃣ Save proposal
        try:
            logger.info("Saving proposal to DB...")

            await prisma.proposal.create(
                data={
                    "rfpVendorId": tracking_id,
                    "rawText": clean_body, # Saving clean body here too
                    "extractedData": Json(structured),
                    "attachments": Json(attachments),
                }
            )

            logger.info("Proposal saved successfully!")
            proposals += 1

        except Exception:
            logger.exception("Error saving Proposal to DB.")

    logger.info("Email sync completed.")
    logger.info(f"Summary: Saved logs={saved}, Skipped={skipped}, Duplicates={duplicates}, Proposals stored={proposals}")

    return {
        "status": "ok",
        "received": len(emails),
        "saved": saved,
        "skipped": skipped,
        "duplicates": duplicates,
        "proposals": proposals
    }


async def sync_email_loop(interval: int):
    """
    Background loop to sync emails repeatedly.
    """
    await asyncio.sleep(3)

    while True:
        try:
            await sync_replies_once()
        except Exception:
            logger.exception("Unhandled error in email sync loop.")

        await asyncio.sleep(interval)