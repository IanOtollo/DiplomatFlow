#!/bin/bash

# MOFA Task Tracker - HTTPS Startup Script

echo "🔒 Starting MOFA Task Tracker with SSL/HTTPS..."
echo "================================================"

# Check if certificates exist
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    echo "❌ SSL certificates not found!"
    echo "Generating new certificates..."
    mkdir -p ssl
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=KE/ST=Nairobi/L=Nairobi/O=MOFA/OU=IT Department/CN=localhost"
    echo "✅ SSL certificates generated!"
fi

# Start the HTTPS server
echo "🚀 Starting HTTPS server..."
echo "🔒 Access your app at: https://localhost:8000"
echo "🔒 Access your app at: https://127.0.0.1:8000"
echo ""
echo "⚠️  Note: You may see a security warning due to self-signed certificate"
echo "   Click 'Advanced' and 'Proceed to localhost' to continue"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 0.0.0.0:8000
