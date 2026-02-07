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
from config import PRICE_THRESHOLD_ALERT, PRICE_THRESHOLD_CHARGE, COOLDOWN_MINUTES, TEST_MODE


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
    
    if TEST_MODE:
        print("⚠️  TEST MODE ENABLED - All checks bypassed")
    
    # Fetch current price
    price = get_current_price()
    if price is None:
        print("Failed to fetch price, exiting")
        return
    
    print(f"Current price: {price}¢/kWh")
    print(f"Alert threshold: {PRICE_THRESHOLD_ALERT}¢/kWh")
    
    state = load_state()
    
    # Build status info for test message
    quiet = is_quiet_hours()
    cooldown_ok = can_send_notification(state)
    price_ok = price < PRICE_THRESHOLD_ALERT
    
    # In TEST MODE: Always send, with status info
    if TEST_MODE:
        status_parts = []
        if quiet:
            status_parts.append("QUIET_HOURS")
        if not cooldown_ok:
            status_parts.append("COOLDOWN")
        if not price_ok:
            status_parts.append(f"PRICE_{price}¢>4¢")
        
        status = " | ".join(status_parts) if status_parts else "ALL_OK"
        message = f"🧪 TEST: {price}¢/kWh [{status}]"
        
        print(f"TEST MODE: Sending regardless of checks")
        sent_count = send_sms_to_all(message)
        if sent_count > 0:
            state["last_notification_time"] = time.time()
            save_state(state)
            print(f"Test alert sent to {sent_count} recipient(s)!")
    else:
        # PRODUCTION MODE: Normal logic
        if quiet:
            print("Quiet hours (12am-6am) - skipping notifications")
            return
        
        if price < PRICE_THRESHOLD_ALERT:
            if cooldown_ok:
                message = f"⚡ ComEd: {price}¢/kWh - Below {PRICE_THRESHOLD_ALERT}¢!"
                
                sent_count = send_sms_to_all(message)
                if sent_count > 0:
                    state["last_notification_time"] = time.time()
                    save_state(state)
                    print(f"Alert sent to {sent_count} recipient(s)!")
            else:
                elapsed = (time.time() - state.get("last_notification_time", 0)) / 60
                print(f"Cooldown active, {COOLDOWN_MINUTES - elapsed:.1f} minutes remaining")
        else:
            print(f"Price {price}¢ is above threshold {PRICE_THRESHOLD_ALERT}¢, no alert needed")
    
    # Log when price is below charge threshold
    if price <= PRICE_THRESHOLD_CHARGE:
        print(f"🔋 Price at or below {PRICE_THRESHOLD_CHARGE}¢ - ideal for Tesla charging!")
    
    print("Done!")


if __name__ == "__main__":
    main()
