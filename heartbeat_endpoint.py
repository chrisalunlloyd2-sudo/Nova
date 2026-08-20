#!/usr/bin/env python3
"""
Nova Heartbeat Endpoint
Provides a simple HTTP endpoint for monitoring the health of the Nova system.
"""

import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class HeartbeatHandler(BaseHTTPRequestHandler):
    """HTTP handler for the heartbeat endpoint."""
    
    def do_GET(self):
        """Handle GET requests to the heartbeat endpoint."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/heartbeat':
            self.send_heartbeat_response()
        elif parsed_path.path == '/status':
            self.send_status_response()
        else:
            self.send_404_response()
    
    def send_heartbeat_response(self):
        """Send a simple heartbeat response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'alive',
            'timestamp': time.time(),
            'message': 'Nova system is running'
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def send_status_response(self):
        """Send a detailed status response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # In a real implementation, this would check various system components
        response = {
            'status': 'healthy',
            'timestamp': time.time(),
            'components': {
                'core_engine': 'running',
                'memory_manager': 'active',
                'network_interface': 'connected',
                'file_system': 'accessible'
            },
            'uptime': self.get_uptime(),
            'message': 'All systems operational'
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def send_404_response(self):
        """Send a 404 Not Found response."""
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'error': 'Not Found',
            'message': 'Endpoint not found. Available endpoints: /heartbeat, /status'
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def get_uptime(self):
        """Calculate system uptime."""
        # This is a placeholder - in a real implementation, you would track actual uptime
        return 'unknown'
    
    def log_message(self, format, *args):
        """Override to disable default logging."""
        pass

class HeartbeatServer:
    """Simple HTTP server for heartbeat monitoring."""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the heartbeat server in a separate thread."""
        self.server = HTTPServer((self.host, self.port), HeartbeatHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        print(f"Heartbeat server started on {self.host}:{self.port}")
    
    def stop(self):
        """Stop the heartbeat server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join()
        print("Heartbeat server stopped")

def main():
    """Main function to run the heartbeat server."""
    server = HeartbeatServer()
    try:
        server.start()
        print("Press Ctrl+C to stop the server")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()

if __name__ == '__main__':
    main()