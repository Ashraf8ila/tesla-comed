"""
SMS Notifier via Email-to-SMS Gateways
Sends SMS messages through email using Gmail SMTP.
Supports multiple carriers.
"""

import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from typing import Optional, List, Tuple


# Email-to-SMS gateways by carrier
CARRIER_GATEWAYS = {
    "tmobile": "tmomail.net",
    "mint": "tmomail.net",        # Mint uses T-Mobile network
    "att": "txt.att.net",
    "verizon": "vtext.com",
    "xfinity": "vtext.com",       # Xfinity uses Verizon network
    "redpocket": "txt.att.net",   # Red Pocket typically uses AT&T
    "sprint": "messaging.sprintpcs.com",
    "metro": "mymetropcs.com",
}


def is_quiet_hours() -> bool:
    """
    Check if current time is within quiet hours (12am-6am).
    Uses the timezone where the script runs.
    """
    current_hour = datetime.now().hour
    return 0 <= current_hour < 6


def get_sms_recipients() -> List[Tuple[str, str]]:
    """
    Parse PHONE_NUMBERS env var into list of (number, gateway) tuples.
    
    Format: "number1:carrier1,number2:carrier2"
    Example: "7162929592:tmobile,6123231366:mint,2243587116:redpocket"
    
    Falls back to PHONE_NUMBER env var for backwards compatibility.
    """
    recipients = []
    
    # New multi-number format
    phone_numbers = os.environ.get("PHONE_NUMBERS", "")
    if phone_numbers:
        for entry in phone_numbers.split(","):
            entry = entry.strip()
            if ":" in entry:
                number, carrier = entry.split(":", 1)
                gateway = CARRIER_GATEWAYS.get(carrier.lower().strip(), "tmomail.net")
                recipients.append((number.strip(), gateway))
            else:
                # Default to T-Mobile if no carrier specified
                recipients.append((entry, "tmomail.net"))
    
    # Backwards compatibility: single PHONE_NUMBER
    single_number = os.environ.get("PHONE_NUMBER", "")
    if single_number and not phone_numbers:
        recipients.append((single_number, "tmomail.net"))
    
    return recipients


def send_sms(
    phone_number: str,
    message: str,
    gateway: str = "tmomail.net",
    gmail_user: Optional[str] = None,
    gmail_app_password: Optional[str] = None
) -> bool:
    """
    Send SMS via email-to-SMS gateway.
    
    Args:
        phone_number: 10-digit phone number (no dashes or spaces)
        message: Message to send (keep under 160 chars for SMS)
        gateway: Carrier's email gateway domain
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
    
    recipient = f"{phone_number}@{gateway}"
    
    msg = MIMEText(message)
    msg["Subject"] = ""  # No subject for SMS
    msg["From"] = gmail_user
    msg["To"] = recipient
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.sendmail(gmail_user, recipient, msg.as_string())
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
    recipients = get_sms_recipients()
    if not recipients:
        print("No phone numbers configured")
        return 0
    
    success_count = 0
    for phone_number, gateway in recipients:
        # TESTING: Only send to 716 numbers
        if not phone_number.startswith("716"):
            print(f"Skipping {phone_number} (testing mode - only 716)")
            continue
        if send_sms(phone_number, message, gateway):
            success_count += 1
    
    return success_count


if __name__ == "__main__":
    # Test the notifier
    print(f"Quiet hours active: {is_quiet_hours()}")
    print(f"Configured recipients: {get_sms_recipients()}")
    print("\nSupported carriers:", list(CARRIER_GATEWAYS.keys()))
