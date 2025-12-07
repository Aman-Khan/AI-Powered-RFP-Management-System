# app/services/email_log_service.py
from prisma import Json
from app.core.prisma import prisma


async def get_all_email_logs():
    """Return all email logs."""
    return await prisma.emaillog.find_many(
        order={'createdAt': 'desc'}
    )


async def get_email_logs_for_vendor(rfp_vendor_id: str):
    """Return all email logs mapped to a specific RFPVendor."""
    return await prisma.emaillog.find_many(
        where={"rfpVendorId": rfp_vendor_id},
        order={'createdAt': 'desc'}
    )


async def delete_email_log(log_id: str):
    """Delete a single email log by ID."""
    return await prisma.emaillog.delete(
        where={"id": log_id}
    )

async def delete_all_email_logs():
    """Delete all records from the EmailLog table."""
    result = await prisma.emaillog.delete_many(
        where={}
    )
    return result