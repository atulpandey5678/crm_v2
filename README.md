# Customer Support Ticket CRM

A COMPLETE, DEPLOYMENT-READY Customer Support CRM System built with FastAPI, SQLite, and TailwindCSS.

## Features

- Create customer support tickets
- View all tickets in a clean dashboard
- Search and filter tickets
- View ticket details
- Update ticket status and add internal notes
- Dark mode toggle
- Responsive, modern SaaS-style UI

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Alembic, Pydantic
- **Frontend:** Jinja2 Templates, TailwindCSS (CDN), AlpineJS, Toastify
- **Database:** SQLite (local), adaptable via `DATABASE_URL`
- **Testing:** Pytest

## Setup & Installation

1. **Clone and enter the directory:**
   ```bash
   git clone <repo-url>
   cd crm_project
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   (Optionally edit `.env` for your local settings)

4. **Run Database Migrations:**
   ```bash
   alembic upgrade head
   ```

## Running Locally

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` in your browser.
API documentation is available at `http://localhost:8000/docs`.

## Testing

Run the automated tests using Pytest:

```bash
pytest
```

## Deployment (Railway)

This project is fully configured for deployment on Railway.

1. Connect your GitHub repository to Railway.
2. Railway will automatically use the `railway.json` and `Procfile`.
3. Add a `DATABASE_URL` environment variable if you plan to use a Postgres plugin on Railway, otherwise it defaults to SQLite (ephemeral on Railway).
4. Deploy!

### Production Checklist

- [x] Environment variables configured
- [x] Database migrations run automatically via startup command
- [x] Secure API endpoints
- [x] Responsive UI
