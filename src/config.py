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
NTFY_TOPIC_CHARGE = "comed-ashraf-charge"

# ============================================================
# Email for iOS Shortcuts Automation
# ============================================================
# Your friend's email address - they'll receive emails with
# subject "START_CHARGE" or "STOP_CHARGE" to trigger iOS automation
CHARGE_EMAIL_RECIPIENT = "kashrafalidev@gmail.com"  # Set this to your friend's email

# ============================================================
# Price Thresholds
# ============================================================
PRICE_THRESHOLD_ALERT = 4.0   # Send notification when price below this (cents)
PRICE_THRESHOLD_CHARGE = 2.0  # Start/stop charging threshold (cents)

# Cooldown between production notifications (minutes)
COOLDOWN_MINUTES = 5

# ============================================================
# Gmail Credentials
# ============================================================
GMAIL_USER = "kashrafaliacad@gmail.com"
GMAIL_APP_PASSWORD = "rubk ihct plcp pauq"
