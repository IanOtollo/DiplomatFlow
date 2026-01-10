#!/bin/bash

# Railway Startup Script for DiplomatFlow

echo "Starting DiplomatFlow deployment..."

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Start the application
echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 4 --timeout 300 mofa_task_tracker.wsgi:application
