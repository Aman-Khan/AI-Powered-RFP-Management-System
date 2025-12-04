from fastapi import APIRouter
from app.services.vendor_service import add_vendor

router = APIRouter()

@router.post("/add")
async def add_vendor_endpoint(name: str, email: str, phone: str):
    return await add_vendor(name, email, phone)
