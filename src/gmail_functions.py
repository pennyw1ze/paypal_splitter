import json
from email import message_from_string
from email.policy import default

import http.server

# Global variables
PORT = 8080

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        email_data = json.loads(post_data)

        email_message = message_from_string(email_data['raw'], policy=default)
        self.handle_email(email_message)

        self.send_response(200)
        self.end_headers()

    def handle_email(self, email_message):
        subject = email_message['subject']
        from_address = email_message['from']
        to_address = email_message['to']
        body = email_message.get_body(preferencelist=('plain', 'html')).get_content()

        # Process the email content as needed
        print(f"Subject: {subject}")
        print(f"From: {from_address}")
        print(f"To: {to_address}")
        print(f"Body: {body}")

def run(server_class=http.server.HTTPServer, handler_class=WebhookHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()