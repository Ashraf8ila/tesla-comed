"""
Configuration - Hardcoded for private repo
"""

# ============================================================
# ntfy.sh Topics (subscribe in the ntfy app)
# ============================================================

# TEST channel - receives ALL runs (for debugging)
NTFY_TOPIC_TEST = "comed-ashraf-test"

# PRODUCTION channel - price drop alerts (threshold, quiet hours, cooldown)
NTFY_TOPIC_PROD = "comed-ashraf-alerts"

# CHARGE channel - for iOS Shortcuts automation
# Title will be exactly "START_CHARGE" or "STOP_CHARGE"
NTFY_TOPIC_CHARGE = "comed-ashraf-charge"

# ============================================================
# Price Thresholds
# ============================================================
PRICE_THRESHOLD_ALERT = 4.0   # Send notification when price below this (cents)
PRICE_THRESHOLD_CHARGE = 2.0  # Ideal for Tesla charging (cents)

# Cooldown between production notifications (minutes)
COOLDOWN_MINUTES = 30

# ============================================================
# Gmail (backup - not currently used)
# ============================================================
GMAIL_USER = "kashrafaliacad@gmail.com"
GMAIL_APP_PASSWORD = "rubk ihct plcp pauq"
