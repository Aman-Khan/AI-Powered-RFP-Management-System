# app/services/proposal_processing.py
from app.services.rfp_extractor import parse_vendor_response
import os
import logging
import sys

# ----------------------------- LOGGER INITIALIZATION ----------------------------- #

logger = logging.getLogger("proposal_processor")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Handler for console output
    ch = logging.StreamHandler(sys.stdout)
    # Set a simple formatter
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# ----------------------------- CORE FUNCTION ----------------------------- #

def process_email_and_attachments(body: str, attachments: list[str]):
    """
    Returns structured proposal OR None if nothing meaningful is extracted.
    """
    logger.info("Starting proposal processing for email and attachments.")
    logger.info(f"Email body length: {len(body)} characters.")
    logger.info(f"Number of attachments: {attachments}.")
    structured = None

    # Try parsing attachments first (PDF / images)
    if attachments:
        logger.info(f"Processing {len(attachments)} attachments...")
        for path in attachments:
            ext = os.path.splitext(path)[1].lower()
            logger.debug(f"Checking attachment: {path} with extension {ext}")

            input_type = None
            if ext in [".pdf"]:
                input_type = "pdf"
            elif ext in [".jpg", ".png", ".jpeg"]:
                input_type = "image"
            
            if input_type:
                logger.info(f"Attempting to parse attachment '{path}' as {input_type}...")
                
                try:
                    structured = parse_vendor_response(path, input_type)
                except Exception as e:
                    logger.error(f"Error parsing attachment {path}: {e}")
                    
                if structured:
                    logger.info(f"Successfully extracted proposal from attachment: {path}")
                    break
            else:
                logger.info(f"Skipping attachment {path}. Unsupported extension: {ext}")
        
    if structured:
        logger.info("Attachment processing finished. Structured data found.")
    else:
        logger.warning("No structured data found in attachments (or no attachments present).")

    # Fallback: parse plain email text
    if not structured:
        logger.info("Falling back to parsing the plain email body as text.")
        try:
            structured = parse_vendor_response(body, "text")
            if structured:
                logger.info("Successfully extracted proposal from email body.")
            else:
                logger.warning("Failed to extract structured data from email body.")
        except Exception as e:
            logger.error(f"Error parsing email body: {e}")

    logger.info("Proposal processing completed.")
    return structured