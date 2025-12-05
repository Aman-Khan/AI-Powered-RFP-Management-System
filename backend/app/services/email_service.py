from pydantic import BaseModel
from fastapi import HTTPException
from app.core.llm.factory import get_llm
from app.core.prisma import prisma
import json
from app.services.email_smtp_service import send_email_smtp
from pydantic import BaseModel

class EmailTemplateRequest(BaseModel):
    rfpId: str


class EmailTemplateResponse(BaseModel):
    subject: str
    content: str
    footer: str


async def generate_email_template_service(rfpId: str):
    # Fetch RFP + user info
    rfp = await prisma.rfp.find_unique(
        where={"id": rfpId},
        include={"user": True}
    )

    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")

    user_name = rfp.user.name if rfp.user else "Procurement Team"

    llm = get_llm()

    # Convert Prisma JSON to Python dict
    structured_rfp = rfp.structuredRequirements or {}

    # Generate email using LLM
    output = await llm.generate_email_template(structured_rfp, user_name)

    # Parse JSON safely
    try:
        cleaned = (
            output.replace("```json", "")
                  .replace("```", "")
                  .strip()
        )
        parsed = json.loads(cleaned)
    except Exception:
        print("LLM RAW OUTPUT:", output)
        raise HTTPException(status_code=500, detail="Invalid JSON from LLM")

    return EmailTemplateResponse(
        subject=parsed.get("subject", f"Request for Proposal – {rfp.title}"),
        content=parsed.get("content", ""),
        footer=parsed.get("footer", f"Thanks & Regards,\n{user_name}")
    )
