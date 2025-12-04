from app.core.prisma import prisma
from app.utils.ids import new_id
from typing import Optional, Dict, Any, List

# ---------------- Add Vendor ----------------
async def add_vendor(name: str, email: Optional[str] = None, phone: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    return await prisma.vendor.create(
        data={
            "id": new_id(),
            "name": name,
            "email": email,
            "phone": phone,
            "metadata": metadata or {}
        }
    )

# ---------------- Get Vendors (Paginated + Search) ----------------
async def get_all_vendors(search: Optional[str] = None, skip: int = 0, limit: int = 20):
    filters = {}

    if search:
        filters = {
            "OR": [
                {"name": {"contains": search, "mode": "insensitive"}},
                {"email": {"contains": search, "mode": "insensitive"}},
                {"phone": {"contains": search, "mode": "insensitive"}},
            ]
        }

    vendors = await prisma.vendor.find_many(
        where=filters,
        skip=skip,
        take=limit,
    )

    # Fallback sorting because orderBy may not be supported
    vendors.sort(key=lambda v: v.createdAt, reverse=True)

    return vendors

# ---------------- Get Vendor ----------------
async def get_vendor(vendor_id: str):
    return await prisma.vendor.find_unique(where={"id": vendor_id})

# ---------------- Update Vendor ----------------
async def update_vendor(vendor_id: str, name=None, email=None, phone=None, metadata=None):
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

# ---------------- Delete Vendor ----------------
async def delete_vendor(vendor_id: str):
    return await prisma.vendor.delete(where={"id": vendor_id})
