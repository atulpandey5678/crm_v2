# Support Ticket CRM

Hey there! This is a simple, lightweight Customer Support CRM that I built to manage support tickets efficiently. The goal was to create something super fast, clean, and production-ready without overcomplicating things. 

You can check out the live version here:
👉 **[Live Demo on Railway](https://web-production-1f9742.up.railway.app/)**

👉 **[GitHub Repository](https://github.com/atulpandey5678/crm_v2)**

## What's under the hood?

I kept the stack modern but straightforward so it runs fast and is easy to maintain:

*   **Backend:** Python with **FastAPI**. It's incredibly fast and makes handling the API routing a breeze.
*   **Database:** **SQLite** paired with **SQLAlchemy** (and Alembic for migrations). It stores all the tickets and notes without the need for a heavy database server.
*   **Frontend:** Standard HTML stitched together with **Jinja2** templates. 
*   **Styling:** **Tailwind CSS**. I used this to create a clean, premium custom theme (Navy, Slate Grey, Beige, and Olive).
*   **Interactivity:** A tiny bit of **Alpine.js** and Vanilla JS for handling things like dark mode toggling and async form submissions.

## Features
*   Create new customer support tickets
*   Dashboard to view and filter tickets by status or search terms
*   Add internal notes to a timeline for each ticket
*   Update ticket statuses (Open, In Progress, Closed)
*   Fully responsive UI with a built-in Dark Mode!

## Running it locally
If you want to spin this up yourself:
1. Clone this repository.
2. Install the requirements: `pip install -r requirements.txt`
3. Run the database migrations: `alembic upgrade head`
4. Start the server: `uvicorn app.main:app --reload`
5. Visit `http://127.0.0.1:8000` in your browser.
