"""
Configuration - Hardcoded for private repo
"""
import os

# ============================================================
# ntfy.sh Topics (subscribe in the ntfy app)
# ============================================================

# TEST channel - receives ALL runs (for debugging)
NTFY_TOPIC_TEST = "comed-ashraf-test"

# PRODUCTION channel - price drop alerts (threshold, quiet hours, cooldown)
NTFY_TOPIC_PROD = "comed-ashraf-alerts"

# CHARGE channel - for iOS Shortcuts automation
NTFY_TOPIC_CHARGE = "comed-ashraf-charge"

# ============================================================
# Email for iOS Shortcuts Automation
# ============================================================
# Email addresses to receive START_CHARGE / STOP_CHARGE emails
CHARGE_EMAIL_RECIPIENTS = [
    # "kashrafalidev@gmail.com",
    "riazyusuff@icloud.com",
]

# ============================================================
# Price Thresholds
# ============================================================
PRICE_THRESHOLD_ALERT = 4.0   # Send notification when price below this (cents)
PRICE_THRESHOLD_CHARGE = 1.9    # Start/stop charging when FREE or negative (0¢ or less)

# Cooldown between production notifications (minutes)
COOLDOWN_MINUTES = 5

# ============================================================
# Gmail Credentials
# ============================================================
GMAIL_USER = os.getenv("GMAIL_USER", "kashrafaliacad@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "rubk ihct plcp pauq")
