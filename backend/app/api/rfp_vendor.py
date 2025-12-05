from fastapi import APIRouter, HTTPException
from app.core.prisma import prisma
from app.utils.ids import new_id
from pydantic import BaseModel

router = APIRouter(tags=["RFPVendor"])


# ----------------------------
# 1️⃣ LIST ALL RFPVendor (FULL DETAIL)
# ----------------------------
@router.get("/")
async def list_all_rfp_vendors():
    rv_list = await prisma.rfpvendor.find_many(
        include={
            "rfp": True,
            "vendor": True,
            "emailLogs": True,
            "proposals": True
        }
    )
    return rv_list


# ----------------------------
# 2️⃣ GET SINGLE RFPVendor BY ID
# ----------------------------
@router.get("/{id}")
async def get_rfp_vendor(id: str):
    rv = await prisma.rfpvendor.find_unique(
        where={"id": id},
        include={
            "rfp": True,
            "vendor": True,
            "emailLogs": True,
            "proposals": True
        }
    )

    if not rv:
        raise HTTPException(status_code=404, detail="RFPVendor not found")

    return rv


# ----------------------------
# 3️⃣ UPDATE STATUS (optional)
# ----------------------------
class StatusUpdate(BaseModel):
    status: str

@router.put("/{id}/status")
async def update_status(id: str, payload: StatusUpdate):
    rv = await prisma.rfpvendor.update(
        where={"id": id},
        data={"status": payload.status}
    )
    return rv


# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from datetime import datetime
# from app.core.prisma import prisma
# from app.utils.ids import new_id

# router = APIRouter(tags=["RFPVendor"])

# # ------------------------
# #  Pydantic Models
# # ------------------------
# class LinkVendorRequest(BaseModel):
#     rfpId: str
#     vendorId: str


# class UpdateVendorStatus(BaseModel):
#     status: str



# # ---------------------------------------------------------
# # 1️⃣ Link Vendor → RFP  (creates RFPVendor row)
# # ---------------------------------------------------------
# @router.post("/link")
# async def link_vendor_to_rfp(payload: LinkVendorRequest):

#     # Prevent duplicates
#     existing = await prisma.rfpvendor.find_first(
#         where={
#             "rfpId": payload.rfpId,
#             "vendorId": payload.vendorId
#         }
#     )
#     if existing:
#         return existing

#     rv = await prisma.rfpvendor.create({
#         "data": {
#             "id": new_id(),
#             "rfpId": payload.rfpId,
#             "vendorId": payload.vendorId,
#             "status": "pending"
#         }
#     })
#     return rv


# # ---------------------------------------------------------
# # 2️⃣ Get all vendors linked with an RFP
# # ---------------------------------------------------------
# @router.get("/rfp/{rfp_id}")
# async def get_vendors_for_rfp(rfp_id: str):
#     vendors = await prisma.rfpvendor.find_many(
#         where={"rfpId": rfp_id},
#         include={
#             "vendor": True,
#             "emailLogs": True,
#             "proposals": True
#         }
#     )
#     return vendors


# @router.get("/")
# async def list_all_rfp_vendors():
#     rv_list = await prisma.rfpvendor.find_many(
#         include={
#             "rfp": True,
#             "vendor": True,
#             "emailLogs": True,
#             "proposals": True
#         }
#     )
#     return rv_list

# # ---------------------------------------------------------
# # 3️⃣ Get single RFPVendor details with full relations
# # ---------------------------------------------------------
# @router.get("/{rv_id}")
# async def get_rfp_vendor_by_id(rv_id: str):
#     rv = await prisma.rfpvendor.find_unique(
#         where={"id": rv_id},
#         include={
#             "rfp": True,
#             "vendor": True,
#             "emailLogs": True,
#             "proposals": True
#         }
#     )

#     if not rv:
#         raise HTTPException(status_code=404, detail="RFPVendor not found")

#     return rv


# # ---------------------------------------------------------
# # 4️⃣ Update Status (sent / reminder_sent / responded / etc.)
# # ---------------------------------------------------------
# @router.put("/{rv_id}/status")
# async def update_status(rv_id: str, payload: UpdateVendorStatus):
#     rv = await prisma.rfpvendor.update(
#         where={"id": rv_id},
#         data={"status": payload.status}
#     )
#     return rv


# # ---------------------------------------------------------
# # 5️⃣ Delete link between RFP and Vendor
# # ---------------------------------------------------------
# @router.delete("/{rv_id}")
# async def delete_rfp_vendor(rv_id: str):
#     await prisma.rfpvendor.delete(where={"id": rv_id})
#     return {"deleted": True, "id": rv_id}

# # ---------------------------------------------------------
# # 6️⃣ Get ALL vendors along with all RFPVendor mappings + RFP details
# # ---------------------------------------------------------
# @router.get("/vendors/all")
# async def get_all_vendors_with_rfps():

#     vendors = await prisma.vendor.find_many(
#         include={
#             "rfpVendors": {
#                 "include": {
#                     "rfp": True  # include full RFP details
#                 }
#             }
#         }
#     )

#     return vendors

