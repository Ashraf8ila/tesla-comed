import sys
import os
import argparse

# Add src to path so we can import config & notifier
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import CHARGE_EMAIL_RECIPIENTS
from notifier import send_email

def main():
    parser = argparse.add_argument_group('Test Email Options')
    # Use argparse module properly
    parser = argparse.ArgumentParser(description="Send a test email with the current price.")
    parser.add_argument('--price', type=str, required=True, help="The current price string to include in the email.")
    
    args = parser.parse_args()
    
    if not CHARGE_EMAIL_RECIPIENTS:
        print("Error: No email recipients configured.")
        sys.exit(1)

    subject = "TEST EMAIL - ComEd Price Alert"
    body = f"This is a test email triggered from the UI.\n\nCurrent ComEd Price: {args.price}¢/kWh"
    
    success = True
    for email in CHARGE_EMAIL_RECIPIENTS:
        if not send_email(email, subject, body):
            print(f"Failed to send test email to {email}")
            success = False
            
    if success:
        print("Successfully sent test emails.")
        sys.exit(0)
    else:
        print("Failed to send some or all test emails.")
        sys.exit(1)

if __name__ == "__main__":
    main()
