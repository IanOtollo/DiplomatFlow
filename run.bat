@echo off
REM Quick run script - installs deps if needed, runs migrations, starts server
cd /d "%~dp0"

echo Checking Python...
python --version 2>nul || (echo Python not found. Install Python 3.10+ and try again. & pause & exit /b 1)

if not exist ".venv_checked" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    echo. > .venv_checked
)
if not exist "db.sqlite3" (
    echo Running migrations...
    python manage.py migrate
    echo Tip: create admin user with: python manage.py createsuperuser
)

echo Starting server at http://127.0.0.1:8000/
python manage.py runserver 0.0.0.0:8000
pause
