from datetime import datetime
from backend.app.core.db_client import prisma
from app.utils.ids import new_id


async def link_vendor_to_rfp(rfp_id: str, vendor_id: str):
    """Create an RFPVendor record."""
    return await prisma.rfpvendor.create({
        "data": {
            "id": new_id(),
            "rfpId": rfp_id,
            "vendorId": vendor_id,
            "status": "pending",
            "sentAt": None
        }
    })


async def mark_rfpvendor_sent(rfp_vendor_id: str):
    """Update vendor record after sending email."""
    return await prisma.rfpvendor.update({
        "where": {"id": rfp_vendor_id},
        "data": {
            "status": "sent",
            "sentAt": datetime.utcnow()
        }
    })


async def get_rfp_vendors(rfp_id: str):
    return await prisma.rfpvendor.find_many(
        where={"rfpId": rfp_id},
        include={"vendor": True, "emailLogs": True}
    )
