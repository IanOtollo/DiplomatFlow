#!/bin/bash

# Create ssl directory if it doesn't exist
mkdir -p ssl

# Generate self-signed certificate if it doesn't exist
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    echo "Generating self-signed certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo "Certificate generated in ssl/ directory"
fi

# Install required packages if not already installed
if ! pip show django-extensions > /dev/null; then
    echo "Installing required packages..."
    pip install django-extensions pyOpenSSL
fi

# Run migrations
echo "Running migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Run the development server with HTTPS
echo "Starting development server with HTTPS..."
echo "Access the site at: https://localhost:8001/"
python3 manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 0.0.0.0:8001
