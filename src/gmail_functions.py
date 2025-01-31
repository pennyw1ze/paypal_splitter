import requests
from google.auth.transport.requests import Request
import pickle
import os

# Base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Token path
token_path = os.path.join(base_path, '..', 'data', 'token.pickle')

def get_latest_email(history_id):
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
    headers = {"Authorization": f"Bearer {access_token}"}

    # Fetch Gmail history based on latest historyId
    history_url = f"https://www.googleapis.com/gmail/v1/users/me/history?startHistoryId={history_id}"
    response = requests.get(history_url, headers=headers)
    history_data = response.json()

    # Extract the latest email message
    latest_message = None
    if "history" in history_data:
        messages = []
        
        for event in history_data["history"]:
            if "messages" in event:
                for message in event["messages"]:
                    messages.append(message)

        # Sort messages by timestamp (internalDate) and get the most recent one
        if messages:
            messages = sorted(messages, key=lambda m: int(m.get("internalDate", 0)))
            latest_message = messages[-1]  # Pick the latest email

    # Fetch full email details
    if latest_message:
        message_id = latest_message["id"]
        email_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}"
        email_response = requests.get(email_url, headers=headers)
        email_data = email_response.json()

        # Check if the message is "UNREAD"
        if "UNREAD" in email_data["labelIds"]:
            # Extract sender, subject, and snippet
            headers_list = email_data["payload"]["headers"]
            sender = next(h["value"] for h in headers_list if h["name"] == "From")
            subject = next(h["value"] for h in headers_list if h["name"] == "Subject")
            snippet = email_data.get("snippet", "")

            print(f"Latest Unread Email Received:")
            print(f"Sender: {sender}")
            print(f"Subject: {subject}")
            print(f"Snippet: {snippet}")

            # Mark the message as "READ"
            modify_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify"
            modify_body = {
                "removeLabelIds": ["UNREAD"]
            }
            requests.post(modify_url, headers=headers, json=modify_body)

get_latest_email(332175)
