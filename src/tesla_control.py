"""
Tesla Control via IFTTT Webhooks
Triggers IFTTT applets to start/stop Tesla charging.
"""

import os
import requests
from typing import Optional


def trigger_ifttt_webhook(event_name: str, key: Optional[str] = None) -> bool:
    """
    Trigger an IFTTT webhook event.
    
    Args:
        event_name: Name of the IFTTT event (e.g., "start_tesla_charge")
        key: IFTTT webhook key (defaults to env var IFTTT_WEBHOOK_KEY)
    
    Returns:
        True if webhook was triggered successfully.
    """
    key = key or os.environ.get("IFTTT_WEBHOOK_KEY")
    
    if not key:
        print("IFTTT webhook key not configured")
        return False
    
    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
    
    try:
        response = requests.post(url, timeout=10)
        if response.ok:
            print(f"IFTTT webhook '{event_name}' triggered successfully")
            return True
        else:
            print(f"IFTTT webhook failed: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error triggering IFTTT webhook: {e}")
        return False


def start_tesla_charging() -> bool:
    """Trigger IFTTT to start Tesla charging."""
    event_name = os.environ.get("IFTTT_START_CHARGE_EVENT", "start_tesla_charge")
    return trigger_ifttt_webhook(event_name)


def stop_tesla_charging() -> bool:
    """Trigger IFTTT to stop Tesla charging."""
    event_name = os.environ.get("IFTTT_STOP_CHARGE_EVENT", "stop_tesla_charge")
    return trigger_ifttt_webhook(event_name)


if __name__ == "__main__":
    print("Tesla Control via IFTTT")
    print(f"Webhook key configured: {bool(os.environ.get('IFTTT_WEBHOOK_KEY'))}")
    print("\nTo test, set IFTTT_WEBHOOK_KEY and run:")
    print("  python tesla_control.py start")
    print("  python tesla_control.py stop")
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            start_tesla_charging()
        elif sys.argv[1] == "stop":
            stop_tesla_charging()
