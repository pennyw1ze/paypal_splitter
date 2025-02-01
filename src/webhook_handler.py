from email import message_from_string
from email.policy import default
import subprocess
import http.server
import sys
from gmail_functions import get_latest_email
import os

# Global variables
PORT = 8080

# Get ngrok URL from ngrok_url.txt file in data folder
def get_ngrok_url():

    # Base path
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Token path
    ngrok_url = os.path.join(base_path, '..', 'data', 'ngrok_url.txt')
    
    with open(ngrok_url, "r") as file:
        ngrok_url = file.read().strip()
    return ngrok_url

# Function to run ngrok server in background
def start_ngrok():
    # Set creation flags for Windows or detach process for Unix-based systems
    creationflags = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
    
    process = subprocess.Popen(
        ["ngrok", "http", f"{get_ngrok_url()}", f"{PORT}"],
        stdout=subprocess.DEVNULL,  # Suppress output
        stderr=subprocess.DEVNULL,  # Suppress errors
        stdin=subprocess.DEVNULL,   # Detach from terminal input
        start_new_session=True,     # Unix: detach process
        creationflags=creationflags # Windows: start in new console
    )
    return process

# Webhook handler class
class WebhookHandler(http.server.BaseHTTPRequestHandler):
    # Handle POST requests
    def do_POST(self):
        get_latest_email()
        self.send_response(200)
        self.end_headers()

    # Handle GET requests
    # Required for ngrok to work
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

# Function to run the server
def run(server_class=http.server.HTTPServer, handler_class=WebhookHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

# Main function
def start_server():
    try:
        # Run the server
        run()
    except KeyboardInterrupt:
        print("\nInterruption received.\nShutting down server...")