from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.ticket import (
    TicketCreate, TicketCreateResponse, 
    TicketResponse, TicketDetailResponse, 
    TicketUpdate, TicketUpdateResponse
)
from app.services import ticket_service
from app.models.ticket import TicketStatus

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

@router.post("", response_model=TicketCreateResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = ticket_service.create_ticket(db, ticket)
    return TicketCreateResponse(
        ticket_id=db_ticket.ticket_id,
        created_at=db_ticket.created_at
    )

@router.get("", response_model=List[TicketResponse])
def get_tickets(
    search: Optional[str] = None, 
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return ticket_service.get_tickets(db, search=search, status=status)

@router.get("/{ticket_id}", response_model=TicketDetailResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    db_ticket = ticket_service.get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=TicketUpdateResponse)
def update_ticket(ticket_id: str, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = ticket_service.update_ticket(db, ticket_id, ticket_update)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketUpdateResponse(
        success=True,
        updated_at=db_ticket.updated_at
    )
