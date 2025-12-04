from fastapi import APIRouter, HTTPException
from typing import List

# Import both the function and the BaseModel from the service file
from app.services.rfp_service import create_rfp, get_all_rfps, RFPCreateRequest, RFPResponse

router = APIRouter(tags=["RFP Management"])

@router.post("/create", response_model=RFPResponse)
async def create_rfp_endpoint(body: RFPCreateRequest):
    """
    Endpoint to create a new RFP.
    Calls the core logic in the rfp_service.
    """
    # Pass the single 'body' object (RFPCreateRequest instance) to the service function.
    return await create_rfp(body)

@router.get("/all/{userId}", response_model=List[RFPResponse])
async def get_all_rfps_endpoint(userId: str):
    """
    Retrieves all RFPs associated with a specific user ID.
    Calls the core logic in the rfp_service.
    """
    return await get_all_rfps(userId)