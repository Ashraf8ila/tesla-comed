"""
Notifier - Push notifications via ntfy.sh + Email for iOS Shortcuts
"""

import smtplib
import requests
from email.mime.text import MIMEText
from config import (
    NTFY_TOPIC_TEST, NTFY_TOPIC_PROD, NTFY_TOPIC_CHARGE,
    GMAIL_USER, GMAIL_APP_PASSWORD, CHARGE_EMAIL_RECIPIENTS
)


def send_to_topic(topic: str, message: str, title: str = "ComEd") -> bool:
    """Send notification to a specific ntfy.sh topic."""
    if not topic:
        print(f"Error: Topic not configured")
        return False
    
    url = f"https://ntfy.sh/{topic}"
    
    try:
        safe_title = title.encode('ascii', 'ignore').decode('ascii') or "ComEd Alert"
        
        response = requests.post(
            url,
            data=message.encode('utf-8'),
            headers={
                "Title": safe_title,
                "Priority": "high",
                "Tags": "zap"
            },
            timeout=10
        )
        
        if response.ok:
            print(f"Sent to ntfy.sh/{topic}")
            return True
        else:
            print(f"ntfy.sh failed: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False


def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email via Gmail SMTP."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Error: Gmail credentials not configured")
        return False
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        print(f"Email sent: {subject} -> {to_email}")
        return True
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        return False


def send_test_notification(message: str, title: str = "TEST") -> bool:
    """Send to TEST channel - always sends, for debugging."""
    return send_to_topic(NTFY_TOPIC_TEST, message, title)


def send_prod_notification(message: str, title: str = "ComEd Alert") -> bool:
    """Send to PRODUCTION channel - for real alerts."""
    return send_to_topic(NTFY_TOPIC_PROD, message, title)


def send_start_charge(price: float) -> bool:
    """
    Send START_CHARGE via ntfy + email for iOS Shortcuts.
    Email subject is exactly "START_CHARGE" for automation matching.
    """
    message = f"Price: {price}c/kWh - Good time to charge!"
    
    # Send ntfy notification
    send_to_topic(NTFY_TOPIC_CHARGE, message, "START_CHARGE")
    
    # Send email to all recipients for iOS Shortcuts automation
    for email in CHARGE_EMAIL_RECIPIENTS:
        send_email(email, "START_CHARGE", message)
    
    return True


def send_stop_charge(price: float) -> bool:
    """
    Send STOP_CHARGE via ntfy + email for iOS Shortcuts.
    Email subject is exactly "STOP_CHARGE" for automation matching.
    """
    message = f"Price: {price}c/kWh - Consider stopping charge."
    
    # Send ntfy notification
    send_to_topic(NTFY_TOPIC_CHARGE, message, "STOP_CHARGE")
    
    # Send email to all recipients for iOS Shortcuts automation
    for email in CHARGE_EMAIL_RECIPIENTS:
        send_email(email, "STOP_CHARGE", message)
    
    return True


def is_quiet_hours() -> bool:
    """Check if current time is within quiet hours (12am-6am)."""
    from datetime import datetime
    current_hour = datetime.now().hour
    return 0 <= current_hour < 6


if __name__ == "__main__":
    print("Testing notifications...")
    send_test_notification("Test message!", "Test Channel")
