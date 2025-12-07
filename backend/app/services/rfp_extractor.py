# app/services/rfp_extractor.py
import os
import re
import json
import logging
import tempfile
from typing import Union, Dict, Any, List, Optional
from dotenv import load_dotenv
import logging
import sys

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)

load_dotenv()

# OCR / Image / PDF tools
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from dateutil import parser as date_parser
import google.generativeai as genai
# These classes are now guaranteed to be available in this scope if the import succeeds
from google.genai.types import Schema, Type, GenerateContentConfig
# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------------------------- SCHEMA & GEMINI CLIENT ----------------------------- #

# Initialize variables to None/Empty outside the try block
RFP_SCHEMA: Optional[Any] = None
GEMINI_CLIENT: Optional[Any] = None

# Gemini SDK
try:


    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_CLIENT = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

    # Define RFP_SCHEMA *inside* the try block where Schema and Type are available
    RFP_SCHEMA = Schema(
        type=Type.OBJECT,
        properties={
            "vendor_name": Schema(type=Type.STRING),
            "contact": Schema(
                type=Type.OBJECT,
                properties={
                    "email": Schema(type=Type.STRING),
                    "phone": Schema(type=Type.STRING),
                    "address": Schema(type=Type.STRING),
                }
            ),
            "items": Schema(
                type=Type.ARRAY,
                items=Schema(
                    type=Type.OBJECT,
                    properties={
                        "name": Schema(type=Type.STRING),
                        "description": Schema(type=Type.STRING),
                        "quantity": Schema(type=Type.STRING),
                        "unit_price": Schema(type=Type.STRING),
                        "total_price": Schema(type=Type.STRING),
                    }
                )
            ),
            "subtotal": Schema(type=Type.STRING),
            "tax": Schema(type=Type.STRING),
            "total_price": Schema(type=Type.STRING),
            "payment_terms": Schema(type=Type.STRING),
            "delivery_date": Schema(type=Type.STRING),
            "warranty": Schema(type=Type.STRING),
            "notes": Schema(type=Type.STRING),
        },
    )
    
except Exception as e:
    # GEMINI_CLIENT and RFP_SCHEMA remain None, but the app can proceed with fallback
    print("Gemini SDK missing or failed to initialize, fallback will be used:", e)


# Logger
logger = logging.getLogger("rfp_extractor")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(ch)

# ----------------------------- HELPERS ----------------------------- #

def _ensure_input_type(t: str) -> str:
    t = (t or "").lower()
    if t not in ("pdf", "image", "text"):
        raise ValueError("input_type must be pdf | image | text")
    return t

def _pdf_to_images(pdf: str, dpi=200):
    try:
        return convert_from_path(pdf, dpi=dpi)
    except Exception as e:
        logger.error("PDF → Image conversion failed: %s", e)
        return []

def _ocr_from_image(img: Image.Image) -> str:
    try:
        return pytesseract.image_to_string(img)
    except Exception as e:
        logger.error("OCR failed: %s", e)
        return ""

def _ocr_file(path: str, input_type: str) -> str:
    if input_type == "pdf":
        pages = _pdf_to_images(path)
        return "\n\n".join(_ocr_from_image(p) for p in pages[:3])
    else:
        return _ocr_from_image(Image.open(path))

def _clean_text(txt: str) -> str:
    txt = txt or ""
    txt = txt.replace("\r", " ").replace("\n", " ")
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()

def _normalize_amount(v) -> Optional[float]:
    if not v:
        return None
    s = str(v).replace(",", "").strip()
    s = re.sub(r"[^\d.\-]", "", s)
    try:
        return float(s)
    except:
        return None

def _normalize_date(v) -> Optional[str]:
    if not v:
        return None
    try:
        return date_parser.parse(v).date().isoformat()
    except:
        return None

# ----------------------------- LLM CALL ----------------------------- #

def _call_gemini(clean: str):
    # Added check for RFP_SCHEMA in addition to GEMINI_CLIENT
    if not GEMINI_CLIENT or not RFP_SCHEMA:
        return None

    try:
        # RFP_SCHEMA is guaranteed to be defined here
        config = GenerateContentConfig(
            response_schema=RFP_SCHEMA,
            response_mime_type="application/json",
        )

        resp = GEMINI_CLIENT.models.generate_content(
            model="gemini-2.5-flash",
            contents=[clean],
            config=config,
        )

        txt = resp.text
        return json.loads(txt)

    except Exception as e:
        logger.error("Gemini parse failed: %s", e)
        return None

# ----------------------------- FALLBACK PARSER ----------------------------- #

def _fallback(text: str):
    """Very simple heuristic parser — works even without AI."""
    return {
        "vendor_name": None,
        "contact": {
            "email": re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text, re.I).group(0)
                     if re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text, re.I) else None,
            "phone": None,
            "address": None
        },
        "items": [],
        "subtotal": None,
        "tax": None,
        "total_price": None,
        "payment_terms": None,
        "delivery_date": None,
        "warranty": None,
        "notes": text[:500],
    }

# ----------------------------- MAIN FUNCTION ----------------------------- #

def parse_vendor_response(input_data: Union[str, bytes], input_type: str) -> Dict[str, Any]:
    """
    Accepts:
        input_data → text OR file path OR bytes
        input_type → pdf | image | text
    Returns structured proposal JSON.
    """
    input_type = _ensure_input_type(input_type)
    
    logger.info("--- Starting Proposal Parsing ---")
    logger.info(f"Input Type: {input_type}")

    raw = ""
    # Extract text
    if input_type == "text":
        raw = input_data.decode("utf-8", "ignore") if isinstance(input_data, bytes) else str(input_data)
        logger.info("Input data treated as raw text.")
    else:
        path = ""
        if isinstance(input_data, bytes):
            # The suffix logic should cover common image types
            suffix = ".pdf" if input_type == "pdf" else ".png" 
            
            # If the user provides the original file extension as context, use it.
            # Otherwise, .png is a safe default for PIL/pytesseract.
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(input_data)
                tmp.flush()
                path = tmp.name
            logger.info(f"Input bytes saved to temporary file: {path}")
        else:
            path = input_data
            logger.info(f"Input data treated as file path: {path}")

        raw = _ocr_file(path, input_type)
        logger.info(f"OCR/File Read successful. Raw text length: {len(raw)}")

        if isinstance(input_data, bytes):
            try: 
                os.remove(path)
                logger.info(f"Temporary file deleted: {path}")
            except Exception as e: 
                logger.error(f"Failed to delete temp file {path}: {e}")

    cleaned = _clean_text(raw)
    logger.info(f"Cleaned text length: {len(cleaned)}. Preview: {cleaned[:100]}...")

    # Try LLM
    structured = _call_gemini(cleaned)

    if structured:
        logger.info("LLM extraction successful.")
        logger.debug(f"LLM Output (Raw): {structured}")
    else:
        logger.warning("LLM extraction failed or returned None. Falling back to heuristic parser.")
        structured = _fallback(cleaned)
        logger.debug(f"Fallback Output (Raw): {structured}")

    # --- Normalize (Important Debugging Point) ---
    logger.info("Starting data normalization...")
    
    # Amount Normalization
    original_subtotal = structured.get("subtotal")
    structured["subtotal"] = _normalize_amount(original_subtotal)
    logger.info(f"Normalize Subtotal: '{original_subtotal}' → {structured['subtotal']}")

    original_tax = structured.get("tax")
    structured["tax"] = _normalize_amount(original_tax)
    logger.info(f"Normalize Tax: '{original_tax}' → {structured['tax']}")

    original_total_price = structured.get("total_price")
    structured["total_price"] = _normalize_amount(original_total_price)
    logger.info(f"Normalize Total Price: '{original_total_price}' → {structured['total_price']}")

    # Date Normalization
    original_delivery_date = structured.get("delivery_date")
    structured["delivery_date"] = _normalize_date(original_delivery_date)
    logger.info(f"Normalize Delivery Date: '{original_delivery_date}' → {structured['delivery_date']}")
    
    logger.info("--- Proposal Parsing Finished ---")
    logger.debug(f"Final Structured Output: {structured}")

    return structured
