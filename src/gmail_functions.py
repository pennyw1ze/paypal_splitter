import requests
from google.auth.transport.requests import Request
import pickle
import os
import re
from bot_functions import received_payment, add_netflix, add_spotify

def get_latest_email():

    # Base path
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Token path
    token_path = os.path.join(base_path, '..', 'data', 'token.pickle')

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
    latest_message_url = "https://www.googleapis.com/gmail/v1/users/me/messages?maxResults=1"
    response = requests.get(latest_message_url, headers=headers)
    latest_message_data = response.json()
    message_id = latest_message_data["messages"][0]["id"]
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
        
        # Let's parse the string
        # Check if the email is from PayPal
        if "assistenza@paypal.it" in sender.lower():
            # Check if the email is about receiving money (Italian)
            if "hai ricevuto denaro" in subject.lower():
                # Parse the snippet to get the amount and the payer using regex
                # We have to find "ti ha inviato", get the previous 2 names, and the amount before "€"
                elems = re.findall(r"([a-zA-Z]+ [a-zA-Z]+) ti ha inviato ([0-9]+,[0-9]+) € EUR", snippet)
                name = elems[0][0].split(" ")[0]
                amount = float(elems[0][1].replace(",", "."))
                received_payment(name, amount)
            elif "netflix" in subject.lower():
                elems = re.findall(r"([0-9]+,[0-9]+) € EUR", snippet)
                amount = float(elems[0].replace(",", "."))
                add_netflix(amount)
            elif "spotify" in subject.lower():
                elems = re.findall(r"([0-9]+,[0-9]+) € EUR", snippet)
                amount = float(elems[0].replace(",", "."))
                add_spotify(amount)
        # Mark the message as "READ"
        modify_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify"
        modify_body = {
            "removeLabelIds": ["UNREAD"]
        }
        requests.post(modify_url, headers=headers, json=modify_body)
    else:
        print("No new unread emails found.")
