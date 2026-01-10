#!/bin/bash

# Activate the virtual environment
source /antenv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 4 mofa_task_tracker.wsgi:application
