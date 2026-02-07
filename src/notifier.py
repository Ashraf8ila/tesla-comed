"""
Notifier - Push notifications via ntfy.sh
Three channels: TEST, PROD, and CHARGE (for iOS Shortcuts)
"""

import requests
from config import NTFY_TOPIC_TEST, NTFY_TOPIC_PROD, NTFY_TOPIC_CHARGE


def send_to_topic(topic: str, message: str, title: str = "ComEd") -> bool:
    """Send notification to a specific ntfy.sh topic."""
    if not topic:
        print(f"Error: Topic not configured")
        return False
    
    url = f"https://ntfy.sh/{topic}"
    
    try:
        # Remove emojis from title for header compatibility
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


def send_test_notification(message: str, title: str = "TEST") -> bool:
    """Send to TEST channel - always sends, for debugging."""
    return send_to_topic(NTFY_TOPIC_TEST, message, title)


def send_prod_notification(message: str, title: str = "ComEd Alert") -> bool:
    """Send to PRODUCTION channel - for real alerts."""
    return send_to_topic(NTFY_TOPIC_PROD, message, title)


def send_start_charge(price: float) -> bool:
    """
    Send START_CHARGE notification for iOS Shortcuts.
    Title is exactly "START_CHARGE" for automation matching.
    """
    message = f"Price: {price}c/kWh - Good time to charge!"
    return send_to_topic(NTFY_TOPIC_CHARGE, message, "START_CHARGE")


def send_stop_charge(price: float) -> bool:
    """
    Send STOP_CHARGE notification for iOS Shortcuts.
    Title is exactly "STOP_CHARGE" for automation matching.
    """
    message = f"Price: {price}c/kWh - Consider stopping charge."
    return send_to_topic(NTFY_TOPIC_CHARGE, message, "STOP_CHARGE")


def is_quiet_hours() -> bool:
    """Check if current time is within quiet hours (12am-6am)."""
    from datetime import datetime
    current_hour = datetime.now().hour
    return 0 <= current_hour < 6


if __name__ == "__main__":
    print("Testing both channels...")
    send_test_notification("Test message!", "Test Channel")
    send_prod_notification("Test message!", "Prod Channel")
