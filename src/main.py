"""
ComEd Price Monitor - Main Entry Point

Channels:
- TEST: Every run with detailed status (for debugging)
- PROD: Price alerts under 4¢ (with cooldown, quiet hours)
- CHARGE: START/STOP when crossing 2¢ threshold
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
                state = json.load(f)
                print(f"Loaded state: {state}")
                return state
        except (json.JSONDecodeError, IOError) as e:
            print(f"Could not load state: {e}")
    return {"last_notification_time": 0, "charging_recommended": False}


def save_state(state: dict) -> None:
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)
        print(f"Saved state: {state}")
    except IOError as e:
        print(f"Warning: Could not save state: {e}")


def get_cooldown_remaining(state: dict) -> float:
    """Get minutes remaining in cooldown, or 0 if cooldown passed."""
    last_time = state.get("last_notification_time", 0)
    elapsed_minutes = (time.time() - last_time) / 60
    remaining = COOLDOWN_MINUTES - elapsed_minutes
    return max(0, remaining)


def main():
    now = datetime.now()
    print(f"[{now.isoformat()}] ComEd Price Monitor")
    
    # Fetch current price
    price = get_current_price()
    if price is None:
        print("Failed to fetch price")
        return
    
    state = load_state()
    quiet = is_quiet_hours()
    cooldown_remaining = get_cooldown_remaining(state)
    cooldown_ok = cooldown_remaining == 0
    charging = state.get("charging_recommended", False)
    
    # Price checks
    below_alert = price < PRICE_THRESHOLD_ALERT      # < 4¢
    below_charge = price <= PRICE_THRESHOLD_CHARGE   # <= 2¢
    
    # ========================================
    # TEST CHANNEL - Detailed status every run
    # ========================================
    status_parts = []
    if quiet:
        status_parts.append("QUIET")
    if not cooldown_ok:
        status_parts.append(f"CD:{cooldown_remaining:.0f}m")
    if charging:
        status_parts.append("CHARGING")
    
    status = " ".join(status_parts) if status_parts else "OK"
    
    # Include all thresholds info
    test_msg = f"{price}c [{status}]\nAlert<{PRICE_THRESHOLD_ALERT}c Charge<={PRICE_THRESHOLD_CHARGE}c"
    send_test_notification(test_msg, "Monitor")
    
    print(f"Price: {price}c | Alert<{PRICE_THRESHOLD_ALERT}c: {below_alert} | Charge<={PRICE_THRESHOLD_CHARGE}c: {below_charge}")
    print(f"Quiet: {quiet} | Cooldown OK: {cooldown_ok} ({cooldown_remaining:.1f}m remaining)")
    
    # ========================================
    # PROD CHANNEL - Under 4¢ alerts
    # ========================================
    if quiet:
        print("PROD: Skipped (quiet hours)")
    elif not below_alert:
        print(f"PROD: Skipped (price {price}c >= {PRICE_THRESHOLD_ALERT}c)")
    elif not cooldown_ok:
        print(f"PROD: Skipped (cooldown {cooldown_remaining:.1f}m remaining)")
    else:
        # All conditions met - send production alert!
        if below_charge:
            prod_msg = f"GREAT PRICE: {price}c/kWh!\nIdeal for charging (under {PRICE_THRESHOLD_CHARGE}c)"
        else:
            prod_msg = f"Low price: {price}c/kWh\nBelow {PRICE_THRESHOLD_ALERT}c threshold"
        
        if send_prod_notification(prod_msg, "ComEd Alert"):
            state["last_notification_time"] = time.time()
            state["last_detected_price"] = price
            state["last_price_time"] = datetime.now().isoformat()
            save_state(state)
            print("PROD: Alert sent!")
    
    # Always save the latest price even if no alert is sent, so the UI is current
    if not (below_alert and not cooldown_ok and not quiet): 
         # Optimization: Don't save on every single skip to reduce IO, 
         # but for this specific request "current charging status and last detected price",
         # we probably want it as fresh as possible.
         # Let's update it at the end of the run regardless of alerts.
         pass

    # Update state with latest price info regardless of notifications
    state["last_detected_price"] = price
    state["last_price_time"] = datetime.now().isoformat()
    save_state(state)
    
    # ========================================
    # CHARGE CHANNEL + EMAIL - Crossing 2¢
    # (Also respects quiet hours)
    # ========================================
    if quiet:
        print("CHARGE: Skipped (quiet hours)")
    elif below_charge and not charging:
        # Price just dropped to/below charge threshold
        send_start_charge(price)
        state["charging_recommended"] = True
        save_state(state)
        print("CHARGE: START sent!")
    elif not below_charge and charging:
        # Price just went above charge threshold
        send_stop_charge(price)
        state["charging_recommended"] = False
        save_state(state)
        print("CHARGE: STOP sent!")
    elif below_charge:
        print("CHARGE: Already in charging mode")
    else:
        print("CHARGE: Price above threshold, not charging")
    
    print("Done!")


if __name__ == "__main__":
    main()
