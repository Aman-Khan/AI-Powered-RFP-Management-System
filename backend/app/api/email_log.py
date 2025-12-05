from fastapi import APIRouter
from app.services.email_log_service import get_logs_by_rfp_vendor

router = APIRouter(tags=["Email Logs"])

@router.get("/email/logs/{rfpVendorId}")
async def get_logs(rfpVendorId: str):
    return await get_logs_by_rfp_vendor(rfpVendorId)
