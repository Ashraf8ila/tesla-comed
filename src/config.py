"""
Configuration - Hardcoded for private repo
"""

# Gmail credentials for sending SMS
GMAIL_USER = "kashrafaliacad@gmail.com"
GMAIL_APP_PASSWORD = "rubk ihct plcp pauq"

# Phone numbers: (number, gateway)
# Supported gateways: tmomail.net (T-Mobile/Mint), vtext.com (Verizon), txt.att.net (AT&T - discontinued)
PHONE_NUMBERS = [
    ("7162929592", "tmomail.net"),   # T-Mobile
    # ("6123231366", "tmomail.net"),   # Mint (uses T-Mobile)
    # ("2243587116", "tmomail.net"),   # Red Pocket (trying T-Mobile gateway)
]

# Price thresholds
PRICE_THRESHOLD_ALERT = 4.0   # Send SMS when price below this (cents)
PRICE_THRESHOLD_CHARGE = 2.0  # Ideal for Tesla charging (cents)

# Cooldown between notifications (minutes)
COOLDOWN_MINUTES = 30
