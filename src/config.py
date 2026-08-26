"""
Configuration - Hardcoded for private repo
"""
import os

# ============================================================
# ntfy.sh Topics (subscribe in the ntfy app)
# ============================================================

# TEST channel - receives ALL runs (for debugging)
NTFY_TOPIC_TEST = os.getenv("NTFY_TOPIC_TEST", "comed-ashraf-test")

# PRODUCTION channel - price drop alerts (threshold, quiet hours, cooldown)
NTFY_TOPIC_PROD = os.getenv("NTFY_TOPIC_PROD", "comed-ashraf-alerts")

# CHARGE channel - for iOS Shortcuts automation
NTFY_TOPIC_CHARGE = os.getenv("NTFY_TOPIC_CHARGE", "comed-ashraf-charge")

# ============================================================
# Email for iOS Shortcuts Automation
# ============================================================
# Email addresses to receive START_CHARGE / STOP_CHARGE emails
# Load from environment variable (comma separated)
_charge_emails_str = os.getenv("CHARGE_EMAILS", "")
CHARGE_EMAIL_RECIPIENTS = [e.strip() for e in _charge_emails_str.split(",") if e.strip()]
if not CHARGE_EMAIL_RECIPIENTS:
    # Default fallback or empty if strictly using secrets
    pass

# ============================================================
# Price Thresholds
# ============================================================
PRICE_THRESHOLD_ALERT = 4.0   # Send notification when price below this (cents)
PRICE_THRESHOLD_CHARGE = 0.0    # Start/stop charging when FREE or negative (0¢ or less)

# Cooldown between production notifications (minutes)
COOLDOWN_MINUTES = 5

# ============================================================
# Gmail Credentials
# ============================================================
GMAIL_USER = os.getenv("GMAIL_USER", "YOUR_EMAIL@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "YOUR_APP_PASSWORD")
