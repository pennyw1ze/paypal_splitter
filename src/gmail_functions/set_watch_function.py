import requests
from google.auth.transport.requests import Request
import pickle
import os

# Base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Token path
token_path = os.path.join(base_path, '../..', 'data', 'token.pickle')

def send_watch_request():

    # Load OAuth credentials
    with open(token_path, "rb") as token:
        creds = pickle.load(token)

    # Refresh token if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    # Get access token
    access_token = creds.token


    # Define the Gmail API Watch Request
    url = "https://www.googleapis.com/gmail/v1/users/me/watch"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "topicName": "projects/quick-nexus-449318-j8/topics/paypal-splitter",  # Replace with your Pub/Sub topic
        "labelIds": ["INBOX"]  # Only get notifications for inbox emails
    }

    # Send the API request
    response = requests.post(url, headers=headers, json=data)
    print(response.json())  # Should return historyId and expiration
