from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import os

from app.routes import api, web
from app.database import engine, Base

app = FastAPI(title="Customer Support CRM")

current_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(current_dir, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates_dir = os.path.join(current_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

app.include_router(api.router)
app.include_router(web.router)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return templates.TemplateResponse(
        request=request,
        name="error.html", 
        context={"status_code": 404, "message": "Page not found"}, 
        status_code=404
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
    return templates.TemplateResponse(
        request=request,
        name="error.html", 
        context={"status_code": 500, "message": "Internal server error"}, 
        status_code=500
    )
