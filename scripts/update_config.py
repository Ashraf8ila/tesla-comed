import argparse
import re
import sys
from pathlib import Path

def update_config(config_path, key, value):
    """
    Updates a specific key in the config file with a new value.
    Preserves comments and formatting.
    """
    try:
        with open(config_path, 'r') as f:
            content = f.read()

        # Determine the replacement string based on the type of value
        if key == 'CHARGE_EMAIL_RECIPIENTS':
            # Value is expected to be a list of strings (e.g., "['email1', 'email2']")
            # We need to format it nicely
            emails = value.split(',')
            formatted_emails = '[\n'
            for email in emails:
                email = email.strip()
                if email:
                    formatted_emails += f'    "{email}",\n'
            formatted_emails += ']'
            replacement = f'{key} = {formatted_emails}'
            
            # Regex for list assignment
            # Matches CHARGE_EMAIL_RECIPIENTS = [ ... ] across multiple lines
            pattern = r'CHARGE_EMAIL_RECIPIENTS\s*=\s*\[.*?\]'
            
        else:
            # Assume number for thresholds
            replacement = f'{key} = {value}'
            pattern = f'{key}\\s*=\\s*[0-9.]+'

        # Perform the substitution
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

        if count == 0:
            print(f"Error: Could not find key '{key}' in {config_path}")
            return False

        with open(config_path, 'w') as f:
            f.write(new_content)
            
        print(f"Successfully updated {key} to {value}")
        return True

    except Exception as e:
        print(f"Error updating {key}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update configuration values in src/config.py')
    parser.add_argument('--emails', help='Comma-separated list of emails')
    parser.add_argument('--alert-threshold', type=float, help='Price threshold for alerts')
    parser.add_argument('--charge-threshold', type=float, help='Price threshold for charging')
    
    args = parser.parse_args()
    
    config_path = Path('src/config.py')
    
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    success = True
    
    if args.emails is not None:
        if not update_config(config_path, 'CHARGE_EMAIL_RECIPIENTS', args.emails):
            success = False

    if args.alert_threshold is not None:
        if not update_config(config_path, 'PRICE_THRESHOLD_ALERT', str(args.alert_threshold)):
            success = False

    if args.charge_threshold is not None:
        if not update_config(config_path, 'PRICE_THRESHOLD_CHARGE', str(args.charge_threshold)):
            success = False

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
