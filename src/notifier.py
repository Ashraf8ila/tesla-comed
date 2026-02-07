"""
Notifier - Push notifications via ntfy.sh
Free, no account needed, works on iOS and Android.
"""

import requests
from config import NTFY_TOPIC


def send_notification(message: str, title: str = "ComEd Price Alert") -> bool:
    """
    Send push notification via ntfy.sh.
    
    Args:
        message: Notification body
        title: Notification title
    
    Returns:
        True if sent successfully
    """
    import base64
    
    if not NTFY_TOPIC:
        print("Error: NTFY_TOPIC not configured")
        return False
    
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    
    try:
        response = requests.post(
            url,
            data=message.encode('utf-8'),
            headers={
                "Title": title.encode('utf-8').decode('latin-1', errors='replace'),
                "Priority": "high",
                "Tags": "zap"
            },
            timeout=10
        )
        
        if response.ok:
            print(f"Notification sent to ntfy.sh/{NTFY_TOPIC}")
            return True
        else:
            print(f"ntfy.sh failed: {response.status_code} - {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"Error sending notification: {e}")
        return False


def is_quiet_hours() -> bool:
    """Check if current time is within quiet hours (12am-6am)."""
    from datetime import datetime
    current_hour = datetime.now().hour
    return 0 <= current_hour < 6


if __name__ == "__main__":
    # Test notification
    print(f"Testing ntfy.sh topic: {NTFY_TOPIC}")
    send_notification("Test notification from ComEd monitor!", "Test")
