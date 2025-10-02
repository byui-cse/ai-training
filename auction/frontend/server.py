#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend files for development.
In production, you'd serve these through a proper web server like Nginx.
"""

import http.server
import socketserver
import os
from urllib.parse import unquote

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle SPA routing - serve index.html for all non-file requests
        path = unquote(self.path)

        # Serve static files normally
        if path.startswith('/static/') or '.' in os.path.basename(path):
            return super().do_GET()

        # For all other requests, serve the index.html
        self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    PORT = 3000

    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving frontend at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            httpd.shutdown()
