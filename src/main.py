"""
ComEd Price Monitor - Main Entry Point
Monitors electricity prices and sends SMS alerts.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

from comed_api import get_current_price
from notifier import send_sms_to_all, is_quiet_hours
from config import PRICE_THRESHOLD_ALERT, PRICE_THRESHOLD_CHARGE, COOLDOWN_MINUTES


# State file for tracking last notification
STATE_FILE = Path(__file__).parent.parent / "state.json"


def load_state() -> dict:
    """Load state from JSON file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"last_notification_time": 0}


def save_state(state: dict) -> None:
    """Save state to JSON file."""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except IOError as e:
        print(f"Warning: Could not save state: {e}")


def can_send_notification(state: dict) -> bool:
    """Check if enough time has passed since last notification."""
    last_time = state.get("last_notification_time", 0)
    elapsed_minutes = (time.time() - last_time) / 60
    return elapsed_minutes >= COOLDOWN_MINUTES


def main():
    """Main monitoring loop iteration."""
    print(f"[{datetime.now().isoformat()}] ComEd Price Monitor running...")
    
    # Check quiet hours (skip if IGNORE_QUIET_HOURS is set)
    if is_quiet_hours() and not os.environ.get("IGNORE_QUIET_HOURS"):
        print("Quiet hours (12am-6am) - skipping notifications")
        return
    
    # Fetch current price
    price = get_current_price()
    if price is None:
        print("Failed to fetch price, exiting")
        return
    
    print(f"Current price: {price}¢/kWh")
    print(f"Alert threshold: {PRICE_THRESHOLD_ALERT}¢/kWh")
    
    state = load_state()
    
    # Check if price is below alert threshold
    if price < PRICE_THRESHOLD_ALERT:
        # TESTING: Cooldown disabled for verification
        # if can_send_notification(state):
        message = f"⚡ ComEd: {price}¢/kWh - Below {PRICE_THRESHOLD_ALERT}¢!"
        
        sent_count = send_sms_to_all(message)
        if sent_count > 0:
            state["last_notification_time"] = time.time()
            save_state(state)
            print(f"Alert sent to {sent_count} recipient(s)!")
    else:
        print(f"Price {price}¢ is above threshold {PRICE_THRESHOLD_ALERT}¢, no alert needed")
    
    # Log when price is below charge threshold
    if price <= PRICE_THRESHOLD_CHARGE:
        print(f"🔋 Price at or below {PRICE_THRESHOLD_CHARGE}¢ - ideal for Tesla charging!")
    
    print("Done!")


if __name__ == "__main__":
    main()
