from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.rfp_service import (
    create_rfp, 
    get_all_rfps, 
    update_rfp,
    delete_rfp,
    get_rfp_by_id,
    RFPCreateRequest, 
    RFPResponse
)

from app.services.email_service import (
    EmailTemplateRequest,
    EmailTemplateResponse,
    generate_email_template_service,
)

router = APIRouter(tags=["RFP Management"])

# Create RFP
@router.post("/create", response_model=RFPResponse)
async def create_rfp_endpoint(body: RFPCreateRequest):
    return await create_rfp(body)

# Get All RFPs (Paginated)
@router.get("/all/{userId}", response_model=List[RFPResponse])
async def get_all_rfps_endpoint(
    userId: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    return await get_all_rfps(userId, skip, limit)

# Update RFP
@router.put("/{rfpId}", response_model=RFPResponse)
async def update_rfp_endpoint(
    rfpId: str,
    structuredRequirements: dict
):
    return await update_rfp(rfpId, structuredRequirements)

# Delete RFP
@router.delete("/{rfpId}", response_model=dict)
async def delete_rfp_endpoint(rfpId: str):
    return await delete_rfp(rfpId)

@router.post("/generate-email", response_model=EmailTemplateResponse)
async def generate_email_template(body: EmailTemplateRequest):
    return await generate_email_template_service(body.rfpId)

@router.get("/{rfpId}", response_model=RFPResponse)
async def get_rfp_by_id_endpoint(rfpId: str):
    rfp = await get_rfp_by_id(rfpId)
    if not rfp:
        raise HTTPException(status_code=404, detail="RFP not found")
    return rfp