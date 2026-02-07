"""
Configuration - Hardcoded for private repo
"""

# ============================================================
# TEST MODE - Set to False when done testing
# ============================================================
TEST_MODE = True

# ntfy.sh topic for push notifications (free, no account needed)
# All users subscribe to this topic in the ntfy app
NTFY_TOPIC = "comed-ashraf-alerts"  # Use a unique name!

# Gmail credentials (keeping for backup/SMS fallback)
GMAIL_USER = "kashrafaliacad@gmail.com"
GMAIL_APP_PASSWORD = "rubk ihct plcp pauq"

# Phone numbers for SMS fallback: (number, gateway)
PHONE_NUMBERS = [
    ("7162929592", "tmomail.net"),   # T-Mobile
    # ("6123231366", "tmomail.net"),   # Mint
    # ("2243587116", "tmomail.net"),   # Red Pocket
]

# Price thresholds
PRICE_THRESHOLD_ALERT = 99.0 if TEST_MODE else 4.0   # High for testing
PRICE_THRESHOLD_CHARGE = 2.0

# Cooldown between notifications (minutes)
COOLDOWN_MINUTES = 30
