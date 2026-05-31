from sqlalchemy.orm import Session
from sqlalchemy import or_, func, case
from app.models.ticket import Ticket, Note, TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate
from typing import List, Optional

def get_next_ticket_id(db: Session) -> str:
    last_ticket = db.query(Ticket).order_by(Ticket.id.desc()).first()
    if not last_ticket:
        return "TKT-001"
    
    try:
        num = int(last_ticket.ticket_id.split("-")[1])
        return f"TKT-{num + 1:03d}"
    except (IndexError, ValueError):
        return f"TKT-{last_ticket.id + 1:03d}"

def create_ticket(db: Session, ticket: TicketCreate) -> Ticket:
    db_ticket = Ticket(
        ticket_id=get_next_ticket_id(db),
        **ticket.model_dump(),
        status=TicketStatus.OPEN
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, search: Optional[str] = None, status: Optional[str] = None) -> List[Ticket]:
    query = db.query(Ticket)
    
    if status and status != "All":
        query = query.filter(Ticket.status == status)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Ticket.ticket_id.ilike(search_term),
                Ticket.customer_name.ilike(search_term),
                Ticket.customer_email.ilike(search_term),
                Ticket.subject.ilike(search_term),
                Ticket.description.ilike(search_term)
            )
        )
        
    return query.order_by(Ticket.created_at.desc()).all()

def get_ticket_by_ticket_id(db: Session, ticket_id: str) -> Optional[Ticket]:
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()

def update_ticket(db: Session, db_ticket: Ticket, update_data: TicketUpdate) -> Ticket:
    if update_data.status:
        db_ticket.status = update_data.status
        
    if update_data.note:
        db.add(Note(ticket_id=db_ticket.id, note_text=update_data.note))
        
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket_stats(db: Session) -> dict:
    stats = db.query(
        func.count(Ticket.id).label("total"),
        func.sum(case((Ticket.status == TicketStatus.OPEN, 1), else_=0)).label("open"),
        func.sum(case((Ticket.status == TicketStatus.IN_PROGRESS, 1), else_=0)).label("in_progress"),
        func.sum(case((Ticket.status == TicketStatus.CLOSED, 1), else_=0)).label("closed")
    ).first()
    
    return {
        "total": stats.total or 0,
        "open": stats.open or 0,
        "in_progress": stats.in_progress or 0,
        "closed": stats.closed or 0
    }
