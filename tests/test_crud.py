import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.models.ticket import TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.crud.ticket_crud import create_ticket, get_tickets, get_ticket_by_ticket_id, update_ticket

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_ticket(db):
    ticket_in = TicketCreate(
        customer_name="John Doe",
        customer_email="john@example.com",
        subject="Login issue",
        description="Cannot login to my account"
    )
    ticket = create_ticket(db, ticket_in)
    assert ticket.customer_name == "John Doe"
    assert ticket.ticket_id == "TKT-001"
    assert ticket.status == TicketStatus.OPEN

def test_get_tickets(db):
    ticket_in = TicketCreate(
        customer_name="Jane Doe",
        customer_email="jane@example.com",
        subject="Payment failed",
        description="My card was declined"
    )
    create_ticket(db, ticket_in)
    
    tickets = get_tickets(db)
    assert len(tickets) == 1
    assert tickets[0].subject == "Payment failed"

    filtered_tickets = get_tickets(db, search="Payment")
    assert len(filtered_tickets) == 1
    
    empty_tickets = get_tickets(db, search="Nonexistent")
    assert len(empty_tickets) == 0

def test_update_ticket(db):
    ticket_in = TicketCreate(
        customer_name="Bob",
        customer_email="bob@example.com",
        subject="Bug report",
        description="App crashes on startup"
    )
    ticket = create_ticket(db, ticket_in)
    
    update_in = TicketUpdate(status=TicketStatus.IN_PROGRESS, note="Looking into it")
    updated_ticket = update_ticket(db, ticket, update_in)
    
    assert updated_ticket.status == TicketStatus.IN_PROGRESS
    assert len(updated_ticket.notes) == 1
    assert updated_ticket.notes[0].note_text == "Looking into it"
