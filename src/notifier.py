"""
SMS Notifier via Email-to-SMS Gateways
Sends SMS messages through email using Gmail SMTP.
"""

import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from typing import Optional

from config import GMAIL_USER, GMAIL_APP_PASSWORD, PHONE_NUMBERS


def is_quiet_hours() -> bool:
    """Check if current time is within quiet hours (12am-6am)."""
    current_hour = datetime.now().hour
    return 0 <= current_hour < 6


def send_sms(phone_number: str, message: str, gateway: str = "tmomail.net") -> bool:
    """
    Send SMS via email-to-SMS gateway.
    
    Returns:
        True if message was sent successfully, False otherwise.
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Error: Gmail credentials not configured")
        return False
    
    recipient = f"{phone_number}@{gateway}"
    
    msg = MIMEText(message)
    msg["Subject"] = ""  # No subject for SMS
    msg["From"] = GMAIL_USER
    msg["To"] = recipient
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipient, msg.as_string())
        print(f"SMS sent to {phone_number} via {gateway}")
        return True
        
    except smtplib.SMTPException as e:
        print(f"Failed to send SMS to {phone_number}: {e}")
        return False


def send_sms_to_all(message: str) -> int:
    """
    Send SMS to all configured recipients.
    
    Returns:
        Number of successfully sent messages.
    """
    if not PHONE_NUMBERS:
        print("No phone numbers configured")
        return 0
    
    success_count = 0
    for phone_number, gateway in PHONE_NUMBERS:
        # TESTING: Only send to 716 numbers
        if not phone_number.startswith("716"):
            print(f"Skipping {phone_number} (testing mode - only 716)")
            continue
        if send_sms(phone_number, message, gateway):
            success_count += 1
    
    return success_count


if __name__ == "__main__":
    print(f"Quiet hours active: {is_quiet_hours()}")
    print(f"Configured recipients: {PHONE_NUMBERS}")
