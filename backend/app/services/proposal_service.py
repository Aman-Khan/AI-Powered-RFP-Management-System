from datetime import datetime
from app.core.prisma import prisma
from app.utils.ids import new_id


async def create_proposal(rfp_vendor_id: str, raw_text: str, extracted_data=None, attachments=None):
    return await prisma.proposal.create({
        "data": {
            "id": new_id(),
            "rfpVendorId": rfp_vendor_id,
            "rawText": raw_text,
            "extractedData": extracted_data or {},
            "attachments": attachments or [],
            "submittedAt": datetime.utcnow()
        }
    })


async def get_proposals_for_vendor(rfp_vendor_id: str):
    return await prisma.proposal.find_many(
        where={"rfpVendorId": rfp_vendor_id}
    )
