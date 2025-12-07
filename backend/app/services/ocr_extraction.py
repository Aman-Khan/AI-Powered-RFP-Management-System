import os
import re
import json
import logging
from typing import Union, Dict, Any, List, Optional
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from dateutil import parser as date_parser
from app.core.config import settings

# Logger
logger = logging.getLogger("ocr_extraction")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(fmt)
    logger.addHandler(ch)

# Tesseract path from env
TESSERACT_PATH = settings.TESSERACT_PATH

if TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Gemini API Setup
GEMINI_CLIENT = None
try:
    from google import genai
    from google.genai.types import Schema, Type, GenerateContentConfig
    from google.genai.errors import APIError
    
    GEMINI_API_KEY = settings.GEMINI_API_KEY

    if GEMINI_API_KEY:
        GEMINI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)
    else:
        logger.warning("GEMINI_API_KEY not found. Falling back to regex parser.")

except ImportError as e:
    logger.error("Gemini SDK not installed: %s", e)

# -------------------------
# Helper Functions
# -------------------------
def _ensure_input_type(input_type: str) -> str:
    if not input_type or input_type.lower() not in ("pdf", "image", "text"):
        raise ValueError("input_type must be one of: 'pdf', 'image', 'text'")
    return input_type.lower()

def _convert_pdf_to_images(pdf_path: str, dpi: int = 200) -> List[Image.Image]:
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
        return pages
    except Exception as e:
        logger.exception("Failed to convert PDF: %s", e)
        return []

def _image_to_text_from_pil(img: Image.Image) -> str:
    try:
        return pytesseract.image_to_string(img) or ""
    except Exception as e:
        logger.exception("Tesseract OCR failed: %s", e)
        return ""

def _ocr_from_path(path: str, input_type: str, page_limit: int = 3) -> str:
    text_parts: List[str] = []
    if input_type == "pdf":
        pages = _convert_pdf_to_images(path)
        for i, page in enumerate(pages[:page_limit]):
            text_parts.append(_image_to_text_from_pil(page))
    else:
        img = Image.open(path)
        text_parts.append(_image_to_text_from_pil(img))
    return "\n".join(text_parts)

def _clean_extracted_text(text: str) -> str:
    if not text: return ""
    s = text.replace("\r", "\n").replace("ﬁ","fi").replace("ﬂ","fl")
    s = re.sub(r"\n+", " ", s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"[\x00-\x1F]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _normalize_amount(value: Optional[Union[str,int,float]]) -> Optional[float]:
    if value is None: return None
    if isinstance(value,(int,float)): return float(value)
    s = str(value).strip()
    if not s: return None
    s = re.sub(r"(?i)(aed|inr|usd|eur|gbp|rs|dhs|sar|rupee|rupees|dirham|\$|€|£|₹)", "", s)
    s = re.sub(r"[,\s]","", s)
    s = re.sub(r"[^\d.\-]","", s)
    if not re.search(r"\d", s): return None
    try: return float(s)
    except Exception:
        m = re.search(r"-?\d+(\.\d+)?", s)
        if m: return float(m.group(0))
    return None

def _normalize_date_to_iso(value: Optional[str]) -> Optional[str]:
    if not value: return None
    s = value.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s): return s
    try:
        dt = date_parser.parse(s, dayfirst=False)
        return dt.date().isoformat()
    except Exception:
        try:
            dt = date_parser.parse(s, dayfirst=True)
            return dt.date().isoformat()
        except Exception:
            return None

# -------------------------
# LLM / fallback parser
# -------------------------
RFP_SCHEMA = Schema(
    type=Type.OBJECT,
    properties={
        "vendor_name": Schema(type=Type.STRING),
        "contact": Schema(type=Type.OBJECT, properties={
            "email": Schema(type=Type.STRING),
            "phone": Schema(type=Type.STRING),
            "address": Schema(type=Type.STRING),
        }),
        "items": Schema(type=Type.ARRAY, items=Schema(type=Type.OBJECT, properties={
            "name": Schema(type=Type.STRING),
            "description": Schema(type=Type.STRING),
            "quantity": Schema(type=Type.STRING),
            "unit_price": Schema(type=Type.STRING),
            "total_price": Schema(type=Type.STRING),
        })),
        "subtotal": Schema(type=Type.STRING),
        "tax": Schema(type=Type.STRING),
        "total_price": Schema(type=Type.STRING),
        "payment_terms": Schema(type=Type.STRING),
        "delivery_date": Schema(type=Type.STRING),
        "warranty": Schema(type=Type.STRING),
        "notes": Schema(type=Type.STRING),
    }
)

def _fallback_regex_parser(text: str) -> Dict[str, Any]:
    result = {
        "vendor_name": None,
        "contact": {"email": None, "phone": None, "address": None},
        "items": [], "subtotal": None, "tax": None, "total_price": None,
        "payment_terms": None, "delivery_date": None, "warranty": None,
        "notes": None
    }

    # Vendor
    m = re.search(r"^(.*?)\s*(?:Contact|Tel|Phone|Email|@)", text, re.IGNORECASE)
    if m: result["vendor_name"] = m.group(1).strip()

    # Email
    email_m = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
    if email_m: result["contact"]["email"] = email_m.group(1)

    # Phone
    phone_m = re.search(r"(\+?\d[\d\-\s\(\)]{7,}\d)", text)
    if phone_m: result["contact"]["phone"] = re.sub(r"\s+"," ",phone_m.group(1))

    # Address
    addr_m = re.search(r"(Address|Location|Office)[:\-]?\s*([A-Za-z0-9,.\-#/ ]{10,300})", text, re.IGNORECASE)
    if addr_m: result["contact"]["address"] = addr_m.group(2).strip()

    # Dates & warranty
    date_m = re.search(r"(Delivery|Delivery Date|Expected Delivery|ETA)[:\-]?\s*([0-9]{1,2}[\/\-\.\s][0-9]{1,2}[\/\-\.\s][0-9]{2,4}|[0-9]{4}-[0-9]{2}-[0-9]{2})", text, re.IGNORECASE)
    if date_m: result["delivery_date"] = _normalize_date_to_iso(date_m.group(2).strip())

    warr_m = re.search(r"Warranty[:\-]?\s*([A-Za-z0-9 \-]{3,100}(year|years|months|limit)?)", text, re.IGNORECASE)
    if warr_m: result["warranty"] = warr_m.group(1).strip()

    # Amounts
    total_m = re.search(r"(Grand Total|TOTAL|Total Due|Total:)[:\-]?\s*([A-Za-z₹$€£0-9,.\s]+)", text, re.IGNORECASE)
    subtotal_m = re.search(r"(Subtotal|Sub-Total|Total Before Tax)[:\-]?\s*([A-Za-z₹$€£0-9,.\s]+)", text, re.IGNORECASE)
    tax_m = re.search(r"(Tax|VAT|GST)[:\-]?\s*([A-Za-z₹$€£0-9,.\s]+)", text, re.IGNORECASE)

    if subtotal_m: result["subtotal"] = _normalize_amount(subtotal_m.group(2))
    if tax_m: result["tax"] = _normalize_amount(tax_m.group(2))
    if total_m: result["total_price"] = _normalize_amount(total_m.group(2))

    # Payment
    pay_m = re.search(r"(Payment Terms|Payment:)[:\-]?\s*([A-Za-z0-9 ,\-\/]{3,50})", text, re.IGNORECASE)
    if pay_m: result["payment_terms"] = pay_m.group(2).strip()

    # Simple items heuristic
    items_found = []
    for m in re.finditer(r"(\d+)\s+(laptops|tablet|monitor|monitors|servers|routers|pcs|pieces|units|keyboards|mouses?)", text, flags=re.IGNORECASE):
        items_found.append({
            "name": m.group(2).strip(),
            "description": None,
            "quantity": m.group(1),
            "unit_price": None,
            "total_price": None
        })
    result["items"] = items_found

    result["notes"] = text[:500].strip()
    return result

def call_llm_api(cleaned_text: str) -> Dict[str, Any]:
    if GEMINI_CLIENT is None:
        return _fallback_regex_parser(cleaned_text)

    llm_prompt = f"""
    You are a precise extraction assistant for vendor quotes (RFP responses).
    Extract data strictly into JSON schema.
    INPUT_TEXT:
    \"\"\"{cleaned_text}\"\"\"
    """
    try:
        config = GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RFP_SCHEMA
        )
        resp = GEMINI_CLIENT.models.generate_content(
            model='gemini-2.5-flash',
            contents=[llm_prompt],
            config=config
        )
        text_out = resp.text if hasattr(resp,"text") else resp.candidates[0].content.parts[0].text
        if not text_out.strip(): raise ValueError("Empty response")
        return json.loads(text_out)
    except Exception as e:
        logger.error("LLM parsing failed, using fallback: %s", e)
        return _fallback_regex_parser(cleaned_text)

# -------------------------
# Main parser function
# -------------------------
def parse_file_service(file_path: str, input_type: str = "image") -> Dict[str, Any]:
    input_type = _ensure_input_type(input_type)

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    try:
        if input_type == "text":
            with open(file_path,"r",encoding="utf-8",errors="ignore") as f:
                raw_text = f.read()
        else:
            raw_text = _ocr_from_path(file_path, input_type)
    except Exception as e:
        return {"error": f"OCR error: {str(e)}"}

    cleaned = _clean_extracted_text(raw_text)
    parsed = call_llm_api(cleaned)

    # Post-process
    output = {
        "vendor_name": parsed.get("vendor_name"),
        "contact": parsed.get("contact", {}),
        "items": parsed.get("items", []),
        "subtotal": _normalize_amount(parsed.get("subtotal")),
        "tax": _normalize_amount(parsed.get("tax")),
        "total_price": _normalize_amount(parsed.get("total_price")),
        "payment_terms": parsed.get("payment_terms"),
        "delivery_date": _normalize_date_to_iso(parsed.get("delivery_date")),
        "warranty": parsed.get("warranty"),
        "notes": parsed.get("notes") or cleaned[:500],
        "error": None
    }

    # Normalize contact
    contact = output.get("contact") or {}
    output["contact"] = {
        "email": contact.get("email"),
        "phone": contact.get("phone"),
        "address": contact.get("address")
    }

    # Normalize items
    normalized_items = []
    for it in output["items"]:
        if not isinstance(it, dict): continue
        normalized_items.append({
            "name": it.get("name"),
            "description": it.get("description"),
            "quantity": str(it.get("quantity")) if it.get("quantity") else None,
            "unit_price": _normalize_amount(it.get("unit_price")),
            "total_price": _normalize_amount(it.get("total_price"))
        })
    output["items"] = normalized_items

    return output

# # -------------------------
# # Demo
# # -------------------------
# if __name__ == "__main__":
#     file_path = r"c:\Users\hp\Desktop\Assessment\AI-Powered-RFP-Management-System\backend\attachments\1.jpeg"
#     parsed_data = parse_file_service(file_path, input_type="image")
#     print(json.dumps(parsed_data, indent=2, default=str))
