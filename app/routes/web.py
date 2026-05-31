from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import ticket_service
from app.models.ticket import TicketStatus
import os

router = APIRouter(include_in_schema=False)

current_dir = os.path.dirname(os.path.realpath(__file__))
templates_dir = os.path.join(os.path.dirname(current_dir), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    search: str = None, 
    status: str = None, 
    db: Session = Depends(get_db)
):
    stats = ticket_service.get_dashboard_stats(db)
    tickets = ticket_service.get_tickets(db, search, status)
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html", 
        context={
            "stats": stats, 
            "tickets": tickets,
            "search": search or "",
            "status": status or "All"
        }
    )

@router.get("/tickets/new", response_class=HTMLResponse)
async def create_ticket_page(request: Request):
    return templates.TemplateResponse(request=request, name="create_ticket.html", context={})

@router.get("/tickets/{ticket_id}", response_class=HTMLResponse)
async def ticket_detail(request: Request, ticket_id: str, db: Session = Depends(get_db)):
    ticket = ticket_service.get_ticket(db, ticket_id)
    if not ticket:
        return templates.TemplateResponse(
            request=request,
            name="error.html", 
            context={"status_code": 404, "message": "Ticket not found"}, 
            status_code=404
        )
        
    return templates.TemplateResponse(
        request=request,
        name="ticket_detail.html", 
        context={"ticket": ticket, "TicketStatus": TicketStatus}
    )
