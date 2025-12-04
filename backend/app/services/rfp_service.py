from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional, List
from prisma import Json
from app.core.prisma import prisma
from app.core.llm.factory import get_llm
from app.utils.ids import new_id
import json

# ----------- Models -----------

class RFPCreateRequest(BaseModel):
    text: str
    userId: str

class RFPResponse(BaseModel):
    id: str
    userId: str
    title: str
    description: Optional[str]
    structuredRequirements: Optional[Dict[str, Any]]

# ----------- Create RFP -----------

async def create_rfp(rfp: RFPCreateRequest):
    user = await prisma.user.find_unique(where={"id": rfp.userId})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    llm = get_llm()

    prompt = f"""
    Convert this procurement description into JSON with:
    - title
    - description
    - structured_requirements {{ budget, items, quantities, warranty, delivery_days, payment_terms }}

    Input: {rfp.text}
    """

    llm_output = await llm.generate_rfp_structure(prompt)

    try:
        cleaned = llm_output.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)
    except Exception:
        raise HTTPException(status_code=500, detail="LLM returned invalid JSON")

    created = await prisma.rfp.create(
        data={
            "id": new_id(),
            "title": parsed.get("title", "Auto-generated RFP"),
            "description": parsed.get("description", rfp.text),
            "structuredRequirements": Json(parsed.get("structured_requirements")),
            "userId": rfp.userId
        }
    )
    
    return created

# ----------- Get RFPs (Paginated + Sorted) -----------

async def get_all_rfps(userId: str, skip: int = 0, limit: int = 20) -> List[RFPResponse]:
    rfps = await prisma.rfp.find_many(
        where={"userId": userId},
        skip=skip,
        take=limit,
        order=[{"createdAt": "desc"}]   # ✅ correct syntax
    )
    return rfps


# ----------- Update RFP -----------

async def update_rfp(rfpId: str, structuredRequirements: dict):
    # Validate JSON
    if not isinstance(structuredRequirements, dict):
        raise HTTPException(status_code=400, detail="structuredRequirements must be a valid JSON object")

    existing = await prisma.rfp.find_unique(where={"id": rfpId})
    if not existing:
        raise HTTPException(status_code=404, detail="RFP not found")

    updated = await prisma.rfp.update(
        where={"id": rfpId},
        data={
            "structuredRequirements": structuredRequirements
        }
    )
    return updated

# ----------- Delete RFP -----------

async def delete_rfp(rfpId: str):
    existing = await prisma.rfp.find_unique(where={"id": rfpId})
    if not existing:
        raise HTTPException(status_code=404, detail="RFP not found")

    await prisma.rfp.delete(where={"id": rfpId})

    return {"success": True, "message": "RFP deleted successfully"}

async def get_rfp_by_id(rfpId: str):
    return await prisma.rfp.find_unique(where={"id": rfpId})
