# app/services/proposal_service.py
from datetime import datetime
from prisma import Json
from app.core.prisma import prisma
from app.utils.ids import new_id


async def create_proposal(rfp_vendor_id: str, raw_text: str, extracted_data=None, attachments=None):
    return await prisma.proposal.create(
        data={
            "id": new_id(),
            "rfpVendorId": rfp_vendor_id,
            "rawText": raw_text,
            "extractedData": Json(extracted_data or {}),
            "attachments": Json(attachments or []),
            "submittedAt": datetime.utcnow(),
        }
    )


async def get_all_proposals():
    return await prisma.proposal.find_many(order={"submittedAt": "desc"})


async def get_proposals_for_vendor(rfp_vendor_id: str):
    return await prisma.proposal.find_many(
        where={"rfpVendorId": rfp_vendor_id},
        order={"submittedAt": "desc"}
    )


async def delete_proposal_by_id(proposal_id: str):
    return await prisma.proposal.delete(
        where={"id": proposal_id}
    )


async def delete_proposals_by_vendor(rfp_vendor_id: str):
    return await prisma.proposal.delete_many(
        where={"rfpVendorId": rfp_vendor_id}
    )
