from fastapi import HTTPException
from pydantic import BaseModel
from app.core.prisma import prisma
from app.utils.ids import new_id
from app.core.llm.factory import get_llm
import json
from typing import Any, Dict, Optional, List
from prisma import Json

# --- Shared Models ---

class RFPCreateRequest(BaseModel):
    text: str
    userId: str

class RFPResponse(BaseModel):
    id: str
    userId: str
    title: str
    description: Optional[str] = None
    structuredRequirements: Optional[Dict[str, Any]] = None

# --- Function to Create a New RFP (Core Logic) ---

async def create_rfp(rfp: RFPCreateRequest):
    user = await prisma.user.find_unique(where={"id": rfp.userId})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    llm = get_llm()
    
    prompt = f"""
    Analyze the following procurement request and convert it into a single JSON object.
    
    The object must have three top-level fields:
    1. 'title': A concise title for the RFP.
    2. 'description': A brief, summary description of the request.
    3. 'structured_requirements': A dictionary containing detailed requirements.
    
    Detailed requirements fields must include: budget, items, quantities, warranty, delivery_days, payment_terms.
    
    Input Request: {rfp.text}
    """
    
    full_structured_text = await llm.generate_rfp_structure(prompt) 

    full_data: Dict[str, Any] | None = None
    
    try:
        full_data = json.loads(full_structured_text)
    except json.JSONDecodeError:
        try:
            cleaned = full_structured_text.strip().replace("```json", "").replace("```", "")
            full_data = json.loads(cleaned)
        except json.JSONDecodeError:
            print(f"ERROR: Could not parse full structured JSON from LLM: {full_structured_text}")
            full_data = None 

    
    title = full_data.get('title', f"Auto-generated RFP for {rfp.text[:50]}...") if full_data else f"Auto-generated RFP for {rfp.text[:50]}..."
    description = full_data.get('description', rfp.text) if full_data else rfp.text
    structured_requirements_data = full_data.get('structured_requirements') if full_data else None

    # Handle nullable Json explicitly for the structured requirements field
    structured_payload = (
        structured_requirements_data 
        if structured_requirements_data is not None 
        else Json.from_none()
    )
    
    created_rfp = await prisma.rfp.create(
        data={
            "id": new_id(),
            "title": title,
            "description": description,
            "structuredRequirements": Json(structured_payload), 
            "userId": rfp.userId
        }
    )

    return created_rfp

# --- Function to Get All RFPs for a User (Core Logic) ---

async def get_all_rfps(userId: str) -> List[RFPResponse]:
    """
    Retrieves all RFPs associated with a specific user ID.
    """
    # Query Prisma for all RFPs where the userId matches the path parameter
    rfps = await prisma.rfp.find_many(
        where={
            "userId": userId
        }
    )
    
    return rfps