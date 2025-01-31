import json
from email import message_from_string
from email.policy import default
import subprocess
import http.server
import sys
import base64
import gmail_functions
import os

# Global variables
PORT = 8080

# Base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Token path
ngrok_url = os.path.join(base_path, '..', 'data', 'ngrok_url.txt')

# Get ngrok URL from ngrok_url.txt file in data folder
def get_ngrok_url():
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
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        email_data = json.loads(post_data)
        decoded_data = base64.urlsafe_b64decode(email_data["message"]["data"]).decode("utf-8")
        history_id = decoded_data["historyId"]
        gmail_functions(history_id)
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



if __name__ == '__main__':
    # Start ngrok
    ngrok_process = start_ngrok()
    print(f"ngrok started with PID: {ngrok_process.pid}")
    try:
        # Run the server
        run()
    except KeyboardInterrupt:
        print("\nInterruption received.\nShutting down server...")
        ngrok_process.terminate()
        ngrok_process.wait()
        print("ngrok process terminated.")