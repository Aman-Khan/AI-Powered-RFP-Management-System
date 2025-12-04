from app.core.prisma import prisma
from app.utils.ids import new_id
from typing import Optional, Dict, Any, List
from prisma import Json

# Add a vendor
async def add_vendor(name: str, email: Optional[str] = None, phone: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    return await prisma.vendor.create(
        data={
            "id": new_id(),
            "name": name,
            "email": email,
            "phone": phone,
            "metadata": Json(metadata) or {}
        }
    )

# Get all vendors
async def get_all_vendors():
    return await prisma.vendor.find_many()

# Get vendor by ID
async def get_vendor(vendor_id: str):
    vendor = await prisma.vendor.find_unique(where={"id": vendor_id})
    return vendor

# Update vendor
async def update_vendor(
    vendor_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    update_data = {}

    if name is not None:
        update_data["name"] = name

    if email is not None:
        update_data["email"] = email

    if phone is not None:
        update_data["phone"] = phone

    if metadata is not None:
        update_data["metadata"] = Json(metadata)

    return await prisma.vendor.update(
        where={"id": vendor_id},
        data=update_data
    )

# Delete vendor
async def delete_vendor(vendor_id: str):
    return await prisma.vendor.delete(where={"id": vendor_id})
