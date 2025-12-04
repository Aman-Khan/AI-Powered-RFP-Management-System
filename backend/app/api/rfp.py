from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rfp_service import create_rfp

router = APIRouter()

class RFPCreateRequest(BaseModel):
    text: str
    userId: str

@router.post("/create")
async def create_rfp_endpoint(body: RFPCreateRequest):
    return await create_rfp(body.text, body.userId)
