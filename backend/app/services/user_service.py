from app.core.prisma import prisma
from typing import Optional, Dict, Any, List

# Create user
async def create_user(email: str, name: str):
    # Check if email exists
    existing = await prisma.user.find_unique(where={"email": email})
    if existing:
        return None
    return await prisma.user.create(
        data={
            "email": email,
            "name": name
        }
    )

# Get all users
async def get_all_users():
    return await prisma.user.find_many()

# Get user by ID
async def get_user(user_id: str):
    return await prisma.user.find_unique(where={"id": user_id})

# Update user
async def update_user(user_id: str, email: Optional[str] = None, name: Optional[str] = None):
    update_data = {}
    if email is not None:
        update_data["email"] = email
    if name is not None:
        update_data["name"] = name

    return await prisma.user.update(where={"id": user_id}, data=update_data)

# Delete user
async def delete_user(user_id: str):
    return await prisma.user.delete(where={"id": user_id})
