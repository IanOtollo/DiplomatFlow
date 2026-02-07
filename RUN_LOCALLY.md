# Run MOFA Task Tracker locally

## Quick start (Windows)

1. **Optional:** Use the run script:
   - Double-click `run.bat`  
   - Or in a terminal: `run.bat`  
   This uses SQLite (no database setup). It will install minimal deps if needed, run migrations, and start the server.

2. **Or run manually:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
   Then open **http://127.0.0.1:8000/**

## First-time setup

- **Create an admin user:**  
  `python manage.py createsuperuser`  
  Then log in at `/users/login/` with that user.

- **Database:**  
  - No `DATABASE_URL` → uses SQLite (`db.sqlite3`) in the project folder. No extra setup.  
  - Set `DATABASE_URL` (e.g. for PostgreSQL) → install `dj-database-url` and `psycopg2-binary` (they are in `requirements.txt`).

## What was fixed

- Task form no longer gets stuck on "Processing" (only AJAX forms show that state).
- Equipment “Assign device” no longer returns 500; form limited to Equipment, Directorate, Room number, Assigned to, Office location.
- Report request page and Contact/About/Features pages have templates and work.
- Password reset/change “done” and “confirm” pages exist and work.
- App runs with SQLite without installing `dj-database-url` (optional import in settings).
