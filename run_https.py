#!/usr/bin/env python3
"""
Django development server with SSL support
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.servers.basehttp import WSGIServer
from django.core.handlers.wsgi import WSGIHandler
import ssl
import socket

def run_https_server():
    """Run Django development server with SSL"""
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mofa_task_tracker.settings')
    django.setup()
    
    # SSL certificate paths
    cert_file = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
    key_file = os.path.join(os.path.dirname(__file__), 'ssl', 'key.pem')
    
    # Check if certificates exist
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("❌ SSL certificates not found!")
        print("Please run: python3 manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem 0.0.0.0:8000")
        return
    
    # Create WSGI application
    application = WSGIHandler()
    
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    
    # Create server
    server = WSGIServer(('0.0.0.0', 8000), application)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    
    print("🚀 Starting MOFA Task Tracker with SSL...")
    print("🔒 HTTPS Server running at: https://localhost:8000")
    print("🔒 HTTPS Server running at: https://127.0.0.1:8000")
    print("⚠️  Note: You may see a security warning due to self-signed certificate")
    print("   Click 'Advanced' and 'Proceed to localhost' to continue")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        server.shutdown()

if __name__ == '__main__':
    run_https_server()
