import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# OAuth scopes required by the Gmail API is both read and modify emails
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"]

# Base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Path to your OAuth JSON file (replace with your file path)
CLIENT_SECRET_FILE = os.path.join(base_path, '../..', 'data', 'secret.json')

# Token path
token_path = os.path.join(base_path, '../..', 'data', 'token.pickle')


def get_credentials():
    creds = None

    # Load token if it exists
    if os.path.exists("token.pickle"):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future use in the absolute path in data/token.pickle
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return creds

# Get access token
def get_access_token():
    credentials = get_credentials()
    access_token = credentials.token
    print(f"Access Token: {access_token}")

get_access_token()
