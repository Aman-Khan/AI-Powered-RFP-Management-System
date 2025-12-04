from fastapi import APIRouter, Request
from app.services.proposal_service import save_vendor_proposal

router = APIRouter()

@router.post("/inbound")
async def inbound_email(request: Request):
    body = await request.form()
    from_email = body.get("from")
    text = body.get("text")

    # TODO: map to the correct rfp_vendor_id
    rfp_vendor_id = "HARDCODED_FOR_NOW"

    await save_vendor_proposal(rfp_vendor_id, text)

    return {"status": "ok"}
