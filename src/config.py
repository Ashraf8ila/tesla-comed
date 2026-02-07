"""
Configuration - Hardcoded for private repo
"""

# ============================================================
# TEST MODE - Set to False when done testing
# ============================================================
TEST_MODE = True

# Gmail credentials for sending SMS
GMAIL_USER = "kashrafaliacad@gmail.com"
GMAIL_APP_PASSWORD = "rubk ihct plcp pauq"

# Phone numbers: (number, gateway)
PHONE_NUMBERS = [
    ("7162929592", "tmomail.net"),   # T-Mobile - TESTING
    # ("6123231366", "tmomail.net"),   # Mint (uses T-Mobile) - UNCOMMENT AFTER TESTING
    # ("2243587116", "tmomail.net"),   # Red Pocket - UNCOMMENT AFTER TESTING
]

# Price thresholds
PRICE_THRESHOLD_ALERT = 99.0 if TEST_MODE else 4.0   # High for testing, 4¢ for production
PRICE_THRESHOLD_CHARGE = 2.0  # Ideal for Tesla charging (cents)

# Cooldown between notifications (minutes)
COOLDOWN_MINUTES = 30
