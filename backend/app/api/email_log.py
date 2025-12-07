# app/api/email_logs.py
from fastapi import APIRouter, HTTPException
from app.services.email_log_service import (
    get_all_email_logs,
    get_email_logs_for_vendor,
    delete_email_log,
    delete_all_email_logs
)

router = APIRouter(tags=["Email Logs"])


# ----------------------------------------------------
# ✔ GET all email logs
# ----------------------------------------------------
@router.get("/email-logs")
async def api_get_all_email_logs():
    return await get_all_email_logs()


# ----------------------------------------------------
# ✔ GET email logs for a specific RFPVendor
# ----------------------------------------------------
@router.get("/email-logs/vendor/{rfpVendorId}")
async def api_get_email_logs_for_vendor(rfpVendorId: str):
    logs = await get_email_logs_for_vendor(rfpVendorId)
    return logs


# ----------------------------------------------------
# ✔ DELETE an email log by ID
# ----------------------------------------------------

@router.delete("/email-all-logs")
async def api_delete_all_email_log():
    try:
        deleted = await delete_all_email_logs()
        return {"status": "deleted"}
    except Exception:
        raise HTTPException(status_code=404, detail="EmailLog not found")



@router.delete("/email-logs/{log_id}")
async def api_delete_email_log(log_id: str):
    try:
        deleted = await delete_email_log(log_id)
        return {"status": "deleted", "id": deleted.id}
    except Exception:
        raise HTTPException(status_code=404, detail="EmailLog not found")

