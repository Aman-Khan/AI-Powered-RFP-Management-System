import email
from email.header import decode_header
from imapclient import IMAPClient
from app.core.config import settings


def decode_mime(value):
    decoded, charset = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8")
    return decoded


def fetch_incoming_emails():
    with IMAPClient(settings.IMAP_HOST) as client:
        client.login(settings.SMTP_USER, settings.SMTP_PASS)
        client.select_folder("INBOX")

        messages = client.search(["UNSEEN"])   # unread emails
        data = client.fetch(messages, ["RFC822"])

        emails = []

        for msgid, msg_data in data.items():
            msg = email.message_from_bytes(msg_data[b"RFC822"])

            subject = decode_mime(msg["Subject"])
            from_email = msg.get("From")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()

            emails.append({
                "id": msgid,
                "from": from_email,
                "subject": subject,
                "body": body
            })

        return emails
