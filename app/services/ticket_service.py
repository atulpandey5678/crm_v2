from sqlalchemy.orm import Session
from app.crud import ticket_crud
from app.schemas.ticket import TicketCreate, TicketUpdate

def create_ticket(db: Session, ticket_in: TicketCreate):
    return ticket_crud.create_ticket(db, ticket_in)

def get_tickets(db: Session, search: str = None, status: str = None):
    return ticket_crud.get_tickets(db, search, status)

def get_ticket(db: Session, ticket_id: str):
    return ticket_crud.get_ticket_by_ticket_id(db, ticket_id)

def update_ticket(db: Session, ticket_id: str, ticket_in: TicketUpdate):
    db_ticket = ticket_crud.get_ticket_by_ticket_id(db, ticket_id)
    if not db_ticket:
        return None
    return ticket_crud.update_ticket(db, db_ticket, ticket_in)
    
def get_dashboard_stats(db: Session):
    return ticket_crud.get_ticket_stats(db)
