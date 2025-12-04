from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from app.services.user_service import create_user, get_all_users, get_user, update_user, delete_user

router = APIRouter(tags=["User Management"])

# --- Request/Response Models ---
class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str

class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

# --- Create User Endpoint ---
@router.post("/create", response_model=UserResponse)
async def create_user_endpoint(user: UserCreateRequest):
    new_user = await create_user(user.email, user.name)
    if not new_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return new_user

# --- Get All Users ---
@router.get("/all", response_model=List[UserResponse])
async def get_all_users_endpoint():
    return await get_all_users()

# --- Get User by ID ---
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- Update User ---
@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: str, payload: UserUpdateRequest):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await update_user(user_id, payload.email, payload.name)
    return updated_user

# --- Delete User ---
@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user_endpoint(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = await delete_user(user_id)
    return deleted_user
