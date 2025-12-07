import asyncio
import traceback
from prisma import Json
from app.services.email_imap_service import fetch_incoming_emails
from app.utils.email_parser import extract_tracking_id
from app.core.prisma import prisma
from app.core.llm.factory import get_llm
from app.services.proposal_processor import process_email_and_attachments


async def sync_replies_once():
    """
    Sync emails once with FULL DEBUG LOGGING.
    """

    print("\n==============================")
    print("🔄 DEBUG: Starting email sync")
    print("==============================\n")

    emails = fetch_incoming_emails(include_seen=True, hours=5)

    print(f"📩 DEBUG: Total fetched emails = {len(emails)}")

    saved = skipped = duplicates = proposals = 0

    for mail in emails:
        print("\n----------------------------------")
        print("📫 DEBUG: Processing new email…")
        print("----------------------------------")

        uid = mail["msgId"]
        body = mail["body"] or ""
        subject = mail["subject"]
        attachments = mail["attachments"]

        print(f"🔹 DEBUG UID(msgId): {uid}")
        print(f"🔹 DEBUG Subject: {subject}")
        preview = body[:150].replace("\n", " ").replace("\r", " ")
        print(f"🔹 DEBUG Body preview: {preview}")
        print(f"🔹 DEBUG Attachments: {attachments}")

        # 1️⃣ Duplicate check
        exists = await prisma.emaillog.find_unique(where={"uid": uid})
        print(f"🔍 DEBUG: Duplicate exists? → {exists is not None}")

        if exists:
            print("⏭️ DEBUG: Skipped (duplicate UID)")
            duplicates += 1
            continue

        # 2️⃣ Extract Ref-ID
        tracking_id = extract_tracking_id(body)
        print(f"🔹 DEBUG Extracted Ref-ID: {tracking_id}")

        if not tracking_id:
            print("⛔ DEBUG: No Ref-ID found → Email skipped")
            skipped += 1
            continue

        rfp_vendor = await prisma.rfpvendor.find_unique(where={"id": tracking_id})
        print(f"🔍 DEBUG Vendor exists? → {rfp_vendor is not None}")

        if not rfp_vendor:
            print("⛔ DEBUG: No matching RFPVendor found")
            skipped += 1
            continue

        # 3️⃣ Save Email Log
        try:
            print("🟢 DEBUG: Saving email log to DB…")
            await prisma.emaillog.create(
                data={
                    "uid": uid,
                    "rfpVendorId": tracking_id,
                    "direction": "incoming",
                    "subject": subject,
                    "body": body,
                    "attachments": Json(attachments),
                }
            )
            print("✅ DEBUG: EmailLog saved")

            saved += 1

        except Exception as e:
            print("❌ ERROR saving EmailLog:", e)
            print(traceback.format_exc())
            continue

        # 4️⃣ Update vendor status
        try:
            print("🟢 DEBUG: Updating vendor status → replied")
            await prisma.rfpvendor.update(
                where={"id": tracking_id},
                data={"status": "replied"}
            )
        except Exception as e:
            print("❌ ERROR updating vendor:", e)
            print(traceback.format_exc())

        # 5️⃣ Proposal detection
        # llm = get_llm()

        # print("🤖 DEBUG: Checking if email is a proposal…")
        # try:
        #     is_prop = await llm.is_proposal_email(body)
        # except Exception as e:
        #     print("❌ ERROR: LLM proposal detection failed:", e)
        #     print(traceback.format_exc())
        #     is_prop = False

        # print(f"🔍 DEBUG: is_proposal_email() returned → {is_prop}")

        # if not is_prop:
        #     print("⏭️ DEBUG: Email is NOT a proposal → stopping here")
        #     continue

        # 6️⃣ Proposal extraction
        try:
            print("🟢 DEBUG: Running proposal extraction…")
            structured = process_email_and_attachments(body, attachments)

            print("📦 DEBUG Extracted structured JSON:")
            print(structured)

        except Exception as e:
            print("❌ ERROR: Proposal extraction failed:", e)
            print(traceback.format_exc())
            continue

        # 7️⃣ Save proposal
        try:
            print("🟢 DEBUG: Saving proposal to DB…")

            await prisma.proposal.create(
                data={
                    "rfpVendorId": tracking_id,
                    "rawText": body,
                    "extractedData": Json(structured),
                    "attachments": Json(attachments),
                }
            )

            print("✅ DEBUG: Proposal saved!")
            proposals += 1

        except Exception as e:
            print("❌ ERROR saving Proposal:", e)
            print(traceback.format_exc())

    print("\n==============================")
    print("📥 FINAL DEBUG SUMMARY")
    print("==============================")
    print(f"Saved logs: {saved}")
    print(f"Skipped: {skipped}")
    print(f"Duplicates: {duplicates}")
    print(f"Proposals stored: {proposals}")
    print("==============================\n")

    return {
        "status": "ok",
        "received": len(emails),
        "saved": saved,
        "skipped": skipped,
        "duplicates": duplicates,
        "proposals": proposals
    }


async def sync_email_loop():
    """
    Background loop to sync every 15 seconds.
    """
    await asyncio.sleep(3)

    while True:
        try:
            await sync_replies_once()
        except Exception as e:
            print("Email sync error:", e)

        await asyncio.sleep(15)
