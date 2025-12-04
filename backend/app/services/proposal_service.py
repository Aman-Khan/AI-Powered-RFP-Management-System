from app.core.prisma import prisma
from app.core.ai_client import extract_vendor_proposal
from app.utils.ids import new_id

async def save_vendor_proposal(rfp_vendor_id: str, raw_text: str):
    extracted = await extract_vendor_proposal(raw_text)
    return await prisma.proposal.create({
        "data": {
            "id": new_id(),
            "rfpVendorId": rfp_vendor_id,
            "rawText": raw_text,
            "extractedData": extracted
        }
    })
