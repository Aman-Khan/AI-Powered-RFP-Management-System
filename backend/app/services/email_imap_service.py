# app/services/email_imap_service.py
import email
import os
from datetime import datetime, timedelta
from email.header import decode_header
from imapclient import IMAPClient

from app.core.config import settings

ATTACH_DIR = "attachments"

if not os.path.exists(ATTACH_DIR):
    os.makedirs(ATTACH_DIR)


def decode_mime(value: str):
    """Decode MIME encoded words (Subject, filenames, etc.)."""
    if not value:
        return ""
    decoded_parts = []
    for decoded, charset in decode_header(value):
        if isinstance(decoded, bytes):
            decoded_parts.append(decoded.decode(charset or "utf-8", errors="ignore"))
        else:
            decoded_parts.append(decoded)
    return "".join(decoded_parts)


def save_attachment(part):
    """Save a single attachment to 'attachments/' folder and return its path."""
    filename = part.get_filename()
    if not filename:
        return None

    filename = decode_mime(filename)
    safe_name = os.path.basename(filename)  # prevent path traversal attacks
    path = os.path.join(ATTACH_DIR, safe_name)

    try:
        with open(path, "wb") as f:
            f.write(part.get_payload(decode=True))
        return path
    except Exception as e:
        print(f"❌ Failed to save attachment {filename}: {e}")
        return None


def extract_body(msg):
    """Extract body (prefer HTML), skipping attachments."""
    body_text = ""
    body_html = ""

    for part in msg.walk():
        # Skip attachments
        if part.get_content_disposition() == "attachment":
            continue

        ctype = part.get_content_type()
        if not ctype.startswith("text/"):
            continue

        content = part.get_payload(decode=True)
        if not content:
            continue

        charset = part.get_content_charset() or "utf-8"

        try:
            decoded = content.decode(charset, errors="ignore")
        except:
            decoded = content.decode("utf-8", errors="ignore")

        if ctype == "text/plain":
            body_text = decoded
        elif ctype == "text/html":
            body_html = decoded

    return body_html or body_text


def fetch_incoming_emails(include_seen=True, hours=2):
    """Fetch emails & treat msgId as UID, save attachment files."""
    try:
        with IMAPClient(settings.IMAP_HOST) as client:
            client.login(settings.SMTP_USER, settings.SMTP_PASS)
            client.select_folder("INBOX")

            since_dt = datetime.utcnow() - timedelta(hours=hours)
            since_str = since_dt.strftime("%d-%b-%Y")

            search_query = ["SINCE", since_str]
            if not include_seen:
                search_query.append("UNSEEN")

            print("🔍 IMAP Criteria:", search_query)

            msg_ids = client.search(search_query)
            print(f"📨 Found {len(msg_ids)} emails")

            if not msg_ids:
                return []

            fetched = client.fetch(msg_ids, ["RFC822"])  # UID is missing → skip

            results = []

            for msgid, data in fetched.items():
                uid = int(msgid)  # 🔥 Use msgid as unique UID

                msg = email.message_from_bytes(data[b"RFC822"])

                # Extract body
                body = extract_body(msg)

                # Extract attachments
                attachments = []
                for part in msg.walk():
                    if part.get_content_disposition() == "attachment":
                        saved_path = save_attachment(part)
                        if saved_path:
                            attachments.append(saved_path)

                print("\n==============================")
                print(f"📧 EMAIL UID (msgid): {uid}")
                print(body[:300].replace("\n", "\\n"))
                print(f"📎 Attachments saved: {attachments}")
                print("------------------------------")

                results.append({
                    "msgId": uid,
                    "subject": decode_mime(msg.get("Subject")),
                    "from": msg.get("From"),
                    "body": body,
                    "attachments": attachments,
                })

            print("📥 Total parsed emails:", len(results))
            return results

    except Exception as e:
        print("❌ ERROR in IMAP:", e)
        return []
