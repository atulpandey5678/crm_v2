import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_ticket_api(client):
    response = client.post(
        "/api/tickets",
        json={
            "customer_name": "Test User",
            "customer_email": "test@example.com",
            "subject": "Test Subject",
            "description": "This is a detailed description of the test issue."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "ticket_id" in data
    assert data["ticket_id"] == "TKT-001"

def test_get_tickets_api(client):
    client.post(
        "/api/tickets",
        json={
            "customer_name": "Alice",
            "customer_email": "alice@example.com",
            "subject": "Issue 1",
            "description": "Description 1 with enough length"
        }
    )
    response = client.get("/api/tickets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_name"] == "Alice"

def test_get_ticket_detail_api(client):
    create_res = client.post(
        "/api/tickets",
        json={
            "customer_name": "Bob",
            "customer_email": "bob@example.com",
            "subject": "Issue 2",
            "description": "Description 2 needs ten chars"
        }
    )
    ticket_id = create_res.json()["ticket_id"]
    
    response = client.get(f"/api/tickets/{ticket_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == ticket_id
    assert data["status"] == "Open"
    assert "notes" in data
    assert len(data["notes"]) == 0

def test_update_ticket_api(client):
    create_res = client.post(
        "/api/tickets",
        json={
            "customer_name": "Charlie",
            "customer_email": "charlie@example.com",
            "subject": "Issue 3",
            "description": "Description 3 must be long enough"
        }
    )
    ticket_id = create_res.json()["ticket_id"]
    
    update_res = client.put(
        f"/api/tickets/{ticket_id}",
        json={
            "status": "In Progress",
            "note": "Started working on this"
        }
    )
    assert update_res.status_code == 200
    
    get_res = client.get(f"/api/tickets/{ticket_id}")
    data = get_res.json()
    assert data["status"] == "In Progress"
    assert len(data["notes"]) == 1
    assert data["notes"][0]["note_text"] == "Started working on this"
