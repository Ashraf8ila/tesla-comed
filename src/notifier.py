"""
SMS Notifier via T-Mobile Email Gateway
Sends SMS messages through email using Gmail SMTP.
"""

import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from typing import Optional


def is_quiet_hours() -> bool:
    """
    Check if current time is within quiet hours (12am-6am).
    Uses the timezone where the script runs.
    """
    current_hour = datetime.now().hour
    return 0 <= current_hour < 6


def send_sms(
    phone_number: str,
    message: str,
    gmail_user: Optional[str] = None,
    gmail_app_password: Optional[str] = None
) -> bool:
    """
    Send SMS via T-Mobile email-to-SMS gateway.
    
    Args:
        phone_number: 10-digit phone number (no dashes or spaces)
        message: Message to send (keep under 160 chars for SMS)
        gmail_user: Gmail address (defaults to env var GMAIL_USER)
        gmail_app_password: Gmail App Password (defaults to env var GMAIL_APP_PASSWORD)
    
    Returns:
        True if message was sent successfully, False otherwise.
    """
    gmail_user = gmail_user or os.environ.get("GMAIL_USER")
    gmail_app_password = gmail_app_password or os.environ.get("GMAIL_APP_PASSWORD")
    
    if not gmail_user or not gmail_app_password:
        print("Error: Gmail credentials not configured")
        return False
    
    # T-Mobile email-to-SMS gateway
    recipient = f"{phone_number}@tmomail.net"
    
    msg = MIMEText(message)
    msg["Subject"] = ""  # No subject for SMS
    msg["From"] = gmail_user
    msg["To"] = recipient
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.sendmail(gmail_user, recipient, msg.as_string())
        print(f"SMS sent to {phone_number}")
        return True
        
    except smtplib.SMTPException as e:
        print(f"Failed to send SMS: {e}")
        return False


if __name__ == "__main__":
    # Test the notifier
    print(f"Quiet hours active: {is_quiet_hours()}")
    print("To test SMS, run with environment variables set:")
    print("  GMAIL_USER=your@gmail.com GMAIL_APP_PASSWORD=xxxx python notifier.py")
