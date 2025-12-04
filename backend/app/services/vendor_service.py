from app.core.prisma import prisma
from app.utils.ids import new_id

async def add_vendor(name, email, phone):
    return await prisma.vendor.create({
        "data": {
            "id": new_id(),
            "name": name,
            "email": email,
            "phone": phone
        }
    })
