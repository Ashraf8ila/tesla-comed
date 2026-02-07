"""
ComEd Price Monitor - Main Entry Point

Sends to TWO channels:
- TEST channel: Always sends (for debugging)
- PROD channel: Follows rules (threshold, quiet hours, cooldown)
"""

import json
import time
from datetime import datetime
from pathlib import Path

from comed_api import get_current_price
from notifier import send_test_notification, send_prod_notification, send_start_charge, send_stop_charge, is_quiet_hours
from config import PRICE_THRESHOLD_ALERT, PRICE_THRESHOLD_CHARGE, COOLDOWN_MINUTES


STATE_FILE = Path(__file__).parent.parent / "state.json"


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"last_notification_time": 0}


def save_state(state: dict) -> None:
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except IOError as e:
        print(f"Warning: Could not save state: {e}")


def can_send_notification(state: dict) -> bool:
    last_time = state.get("last_notification_time", 0)
    elapsed_minutes = (time.time() - last_time) / 60
    return elapsed_minutes >= COOLDOWN_MINUTES


def main():
    print(f"[{datetime.now().isoformat()}] ComEd Price Monitor")
    
    # Fetch current price
    price = get_current_price()
    if price is None:
        print("Failed to fetch price")
        return
    
    print(f"Price: {price}¢/kWh | Threshold: {PRICE_THRESHOLD_ALERT}¢")
    
    state = load_state()
    quiet = is_quiet_hours()
    cooldown_ok = can_send_notification(state)
    price_ok = price < PRICE_THRESHOLD_ALERT
    
    # ========================================
    # TEST CHANNEL - Always sends with status
    # ========================================
    status_parts = []
    if quiet:
        status_parts.append("QUIET")
    if not cooldown_ok:
        status_parts.append("COOLDOWN")
    if not price_ok:
        status_parts.append(f">{PRICE_THRESHOLD_ALERT}c")
    
    status = " | ".join(status_parts) if status_parts else "OK"
    test_msg = f"{price}c/kWh [{status}]"
    send_test_notification(test_msg, "ComEd Monitor")
    
    # ========================================
    # PROD CHANNEL - Follows all rules
    # ========================================
    if quiet:
        print("Quiet hours - skipping prod notification")
    elif not price_ok:
        print(f"Price above threshold - skipping prod notification")
    elif not cooldown_ok:
        elapsed = (time.time() - state.get("last_notification_time", 0)) / 60
        print(f"Cooldown: {COOLDOWN_MINUTES - elapsed:.1f} min remaining")
    else:
        # All conditions met - send production alert!
        prod_msg = f"Price dropped to {price}c/kWh!\nBelow {PRICE_THRESHOLD_ALERT}c threshold."
        if send_prod_notification(prod_msg, "Low Price Alert"):
            state["last_notification_time"] = time.time()
            save_state(state)
            print("Production alert sent!")
    
    # ========================================
    # CHARGE CHANNEL - For iOS Shortcuts
    # ========================================
    was_charging = state.get("charging_recommended", False)
    should_charge = price <= PRICE_THRESHOLD_CHARGE
    
    if should_charge and not was_charging:
        # Price just dropped below charge threshold - send START
        send_start_charge(price)
        state["charging_recommended"] = True
        save_state(state)
        print("START_CHARGE sent!")
    elif not should_charge and was_charging:
        # Price just went above charge threshold - send STOP
        send_stop_charge(price)
        state["charging_recommended"] = False
        save_state(state)
        print("STOP_CHARGE sent!")
    elif should_charge:
        print(f"Charging recommended (already notified)")
    
    print("Done!")


if __name__ == "__main__":
    main()
