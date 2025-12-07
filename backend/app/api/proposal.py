# app/api_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.services.proposal_service import (
    create_proposal,
    get_all_proposals,
    get_proposals_for_vendor,
    delete_proposal_by_id,
    delete_proposals_by_vendor,
)

router = APIRouter(tags=["Proposal"])


class CreateProposalInput(BaseModel):
    rfpVendorId: str
    rawText: str
    extractedData: Optional[Dict[str, Any]] = None
    attachments: Optional[List[Any]] = None


# ---------------- CREATE -----------------
@router.post("/create")
async def create_proposal_api(payload: CreateProposalInput):
    return await create_proposal(
        payload.rfpVendorId,
        payload.rawText,
        payload.extractedData,
        payload.attachments,
    )


# ---------------- READ -----------------
@router.get("/all")
async def list_all_proposals():
    return await get_all_proposals()


@router.get("/vendor/{rfpVendorId}")
async def get_vendor_proposals_api(rfpVendorId: str):
    return await get_proposals_for_vendor(rfpVendorId)


# ---------------- DELETE -----------------
@router.delete("/delete/{proposalId}")
async def delete_proposal_api(proposalId: str):
    return await delete_proposal_by_id(proposalId)


@router.delete("/delete/vendor/{rfpVendorId}")
async def delete_vendor_proposals_api(rfpVendorId: str):
    deleted = await delete_proposals_by_vendor(rfpVendorId)
    return {"deletedCount": deleted.count}
