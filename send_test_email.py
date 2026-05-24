from __future__ import annotations

import base64
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
BUYER_NAME = os.getenv("BUYER_NAME", "Alex")
BUYER_EMAIL = os.getenv("BUYER_EMAIL", "alex@example.com")
USE_GMAIL_API = os.getenv("USE_GMAIL_API", "false").strip().lower() in ("1", "true", "yes")
GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
GMAIL_TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE", "token.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def build_message() -> EmailMessage:
    if not EMAIL_USERNAME or not EMAIL_TO:
        raise ValueError("EMAIL_USERNAME and EMAIL_TO must be set in the environment.")

    msg = EmailMessage()
    msg["Subject"] = "Inquiry: Cutting Board Purchase"
    msg["From"] = EMAIL_USERNAME
    msg["To"] = EMAIL_TO
    msg["Reply-To"] = BUYER_EMAIL
    msg.set_content(
        f"""Hello,

My name is {BUYER_NAME}, and I'm interested in purchasing one of your cutting boards. I would like to know:

- Available sizes and wood options
- Current price
- Shipping costs
- Estimated delivery timeline

Please let me know if you have anything in stock and how I can place an order.

Thank you,
{BUYER_NAME}
"""
    )
    return msg


def send_message_smtp(message: EmailMessage) -> None:
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_USERNAME and EMAIL_PASSWORD are required for SMTP sending.")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        smtp.send_message(message)


def get_gmail_api_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists(GMAIL_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_FILE, SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        return creds

    if not os.path.exists(GMAIL_CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"Missing Gmail credentials file: {GMAIL_CREDENTIALS_FILE}. "
            "Create OAuth credentials in Google Cloud Console and download the file."
        )

    flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    with open(GMAIL_TOKEN_FILE, "w", encoding="utf-8") as token_file:
        token_file.write(creds.to_json())
    return creds


def send_message_gmail_api(message: EmailMessage) -> None:
    from googleapiclient.discovery import build

    creds = get_gmail_api_credentials()
    service = build("gmail", "v1", credentials=creds)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_result = (
        service.users()
        .messages()
        .send(userId="me", body={"raw": raw_message})
        .execute()
    )
    print("Gmail API message sent, id:", send_result.get("id"))


def send_message(message: EmailMessage) -> None:
    if USE_GMAIL_API:
        send_message_gmail_api(message)
    else:
        send_message_smtp(message)


if __name__ == "__main__":
    try:
        email_message = build_message()
        send_message(email_message)
        print(f"Test email sent to {EMAIL_TO}")
    except Exception as exc:
        print("ERROR: Could not send test email:", exc)
        raise
