from fastapi import APIRouter
from pydantic import BaseModel
from app.services.proposal_service import create_proposal, get_proposals_for_vendor

router = APIRouter(tags=["Proposal"])

class CreateProposalInput(BaseModel):
    rfpVendorId: str
    rawText: str
    extractedData: dict | None = None


@router.post("/proposal/create")
async def create_proposal_api(payload: CreateProposalInput):
    return await create_proposal(
        payload.rfpVendorId,
        payload.rawText,
        payload.extractedData
    )


@router.get("/proposal/{rfpVendorId}")
async def get_vendor_proposals(rfpVendorId: str):
    return await get_proposals_for_vendor(rfpVendorId)
