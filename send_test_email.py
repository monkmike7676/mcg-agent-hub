from __future__ import annotations

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


def send_message(message: EmailMessage) -> None:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        if EMAIL_USERNAME and EMAIL_PASSWORD:
            smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        smtp.send_message(message)


if __name__ == "__main__":
    try:
        email_message = build_message()
        send_message(email_message)
        print(f"Test email sent to {EMAIL_TO}")
    except Exception as exc:
        print("ERROR: Could not send test email:", exc)
        raise
