# app/schemas/email_log.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any, Dict

class EmailLogModel(BaseModel):
    """Schema for transferring EmailLog data (used for API responses)."""
    
    id: str = Field(..., description="Unique ID of the email log.")
    uid: int = Field(..., description="Unique Identifier (UID) from the IMAP server.")
    rfpVendorId: Optional[str] = Field(None, description="ID of the related RFP Vendor, if applicable.")
    direction: str = Field(..., description="Direction of the email (e.g., 'incoming', 'outgoing').")
    subject: Optional[str] = Field(None, description="Email subject line.")
    body: Optional[str] = Field(None, description="Email body content.")
    
    attachments: Optional[List[str]] = Field(None, description="List of file paths for attachments.")
    
    createdAt: datetime = Field(..., description="Timestamp of creation.")

    class Config:
        from_attributes = True