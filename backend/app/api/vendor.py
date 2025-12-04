from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from app.services.vendor_service import (
    add_vendor,
    get_all_vendors,
    get_vendor,
    update_vendor,
    delete_vendor
)

class VendorCreateRequest(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class VendorUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

router = APIRouter(tags=["Vendor Management"])

# Add vendor
@router.post("/add")
async def add_vendor_endpoint(body: VendorCreateRequest):
    return await add_vendor(body.name, body.email, body.phone)

# Get vendors with pagination + search
@router.get("/")
async def get_all_vendors_endpoint(
    search: Optional[str] = Query(None, description="Search by name, email, phone"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    return await get_all_vendors(search=search, skip=skip, limit=limit)

# Get vendor by ID
@router.get("/{vendor_id}")
async def get_vendor_endpoint(vendor_id: str):
    vendor = await get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

# Update vendor
@router.put("/{vendor_id}")
async def update_vendor_endpoint(vendor_id: str, body: VendorUpdateRequest):
    vendor = await get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return await update_vendor(
        vendor_id,
        name=body.name,
        email=body.email,
        phone=body.phone
    )

# Delete vendor
@router.delete("/{vendor_id}")
async def delete_vendor_endpoint(vendor_id: str):
    vendor = await get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return await delete_vendor(vendor_id)
