# app/utils/email_parser.py
import re

REF_REGEX = re.compile(r"Ref-ID[:\s]*([a-zA-Z0-9\-]+)", re.IGNORECASE)

def extract_tracking_id(body: str):
    if not body:
        return None
    match = REF_REGEX.search(body)
    return match.group(1) if match else None
