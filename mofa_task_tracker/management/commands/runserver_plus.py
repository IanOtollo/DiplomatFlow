from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.servers.basehttp import WSGIServer
import ssl
import os
from pathlib import Path

class Command(RunserverCommand):
    help = 'Starts a lightweight Web server for development with HTTPS support.'

    def handle(self, *args, **options):
        # Set up SSL context
        cert_file = Path(__file__).resolve().parent.parent.parent.parent / 'ssl' / 'cert.pem'
        key_file = Path(__file__).resolve().parent.parent.parent.parent / 'ssl' / 'key.pem'
        
        if not cert_file.exists() or not key_file.exists():
            self.stdout.write(
                self.style.ERROR('SSL certificate or key not found. Please run the setup_ssl.sh script first.')
            )
            return

        # Monkey patch the WSGI server to use SSL
        original_handler = WSGIServer.get_request
        def ssl_wrap_socket(self, *args, **kwargs):
            client, addr = original_handler(self, *args, **kwargs)
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile=str(cert_file), keyfile=str(key_file))
            return ssl_context.wrap_socket(client, server_side=True), addr
        
        WSGIServer.get_request = ssl_wrap_socket
        
        # Set the default port to 8001 for HTTPS
        if not options.get('addrport'):
            options['addrport'] = '0.0.0.0:8001'
        
        self.stdout.write(
            self.style.SUCCESS('Starting development server with HTTPS support at https://%s/' % options['addrport'])
        )
        
        # Call the parent handle method
        super().handle(*args, **options)
