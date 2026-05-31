from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.models.ticket import TicketStatus

class NoteBase(BaseModel):
    note_text: str = Field(..., min_length=1)

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    ticket_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TicketBase(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: EmailStr
    subject: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=10)

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    note: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    ticket_id: str
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TicketDetailResponse(TicketResponse):
    notes: List[NoteResponse] = []

class TicketCreateResponse(BaseModel):
    ticket_id: str
    created_at: datetime

class TicketUpdateResponse(BaseModel):
    success: bool
    updated_at: datetime
