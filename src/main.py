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
from tesla_control import start_tesla_charging


# State file for tracking last notification
STATE_FILE = Path(__file__).parent.parent / "state.json"


def get_config():
    """Read configuration from environment variables."""
    return {
        "price_threshold_alert": float(os.environ.get("PRICE_THRESHOLD_ALERT", "4.0")),
        "price_threshold_charge": float(os.environ.get("PRICE_THRESHOLD_CHARGE", "2.0")),
        "cooldown_minutes": int(os.environ.get("COOLDOWN_MINUTES", "30")),
        "phone_number": os.environ.get("PHONE_NUMBER", ""),
    }


def load_state() -> dict:
    """Load state from JSON file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"last_notification_time": 0, "last_charge_command_time": 0}


def save_state(state: dict) -> None:
    """Save state to JSON file."""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except IOError as e:
        print(f"Warning: Could not save state: {e}")


def can_send_notification(state: dict, cooldown_minutes: int) -> bool:
    """Check if enough time has passed since last notification."""
    last_time = state.get("last_notification_time", 0)
    elapsed_minutes = (time.time() - last_time) / 60
    return elapsed_minutes >= cooldown_minutes


def main():
    """Main monitoring loop iteration."""
    print(f"[{datetime.now().isoformat()}] ComEd Price Monitor running...")
    
    # Check quiet hours
    if is_quiet_hours() and not os.environ.get("IGNORE_QUIET_HOURS"):
        print("Quiet hours (12am-6am) - skipping notifications")
        return
    
    # Load config at runtime (after .env is loaded)
    config = get_config()
    
    # Fetch current price
    price = get_current_price()
    if price is None:
        print("Failed to fetch price, exiting")
        return
    
    print(f"Current price: {price}¢/kWh")
    print(f"Alert threshold: {config['price_threshold_alert']}¢/kWh")
    print(f"Charge threshold: {config['price_threshold_charge']}¢/kWh")
    
    state = load_state()
    
    # Check if price is below alert threshold
    if price < config["price_threshold_alert"]:
        if can_send_notification(state, config["cooldown_minutes"]):
            message = f"⚡ ComEd: {price}¢/kWh - Below {config['price_threshold_alert']}¢!"
            
            sent_count = send_sms_to_all(message)
            if sent_count > 0:
                state["last_notification_time"] = time.time()
                save_state(state)
                print(f"Alert sent to {sent_count} recipient(s)!")
        else:
            mins_remaining = config["cooldown_minutes"] - ((time.time() - state.get("last_notification_time", 0)) / 60)
            print(f"Cooldown active, {mins_remaining:.1f} minutes remaining")
    
    # Check if price is below charge threshold - trigger Tesla charging via IFTTT
    if price <= config["price_threshold_charge"]:
        # Only trigger if we haven't recently (use same cooldown as notifications)
        last_charge_time = state.get("last_charge_command_time", 0)
        charge_cooldown = (time.time() - last_charge_time) / 60 >= config["cooldown_minutes"]
        
        if charge_cooldown:
            print(f"🔋 Price at or below {config['price_threshold_charge']}¢ - triggering Tesla charging")
            if start_tesla_charging():
                state["last_charge_command_time"] = time.time()
                save_state(state)
        else:
            print(f"🔋 Price is low, but charge command already sent recently")
    
    print("Done!")


if __name__ == "__main__":
    main()
