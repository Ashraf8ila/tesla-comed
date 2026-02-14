import argparse
import re
import sys
from pathlib import Path

def update_config(config_path, key, value, append=False):
    """
    Updates a specific key in the config file with a new value.
    Preserves comments and formatting.
    If append is True, adds the value to a list instead of replacing it.
    """
    try:
        with open(config_path, 'r') as f:
            content = f.read()

        if key == 'CHARGE_EMAIL_RECIPIENTS':
            # Regex for list assignment
            # Matches CHARGE_EMAIL_RECIPIENTS = [ ... ] across multiple lines
            pattern = r'(CHARGE_EMAIL_RECIPIENTS\s*=\s*\[)(.*?)(\])'
            match = re.search(pattern, content, re.DOTALL)
            
            if not match:
                print(f"Error: Could not find key '{key}' in {config_path}")
                return False

            current_list_str = match.group(2)
            
            if append:
                # Value is a single email to add
                new_email = value.strip()
                if not new_email:
                    print("Error: Empty email provided")
                    return False
                
                # Check if email already exists (simple string check to avoid parsing issues)
                if f'"{new_email}"' in current_list_str or f"'{new_email}'" in current_list_str:
                    print(f"Email '{new_email}' already exists. Skipping.")
                    return True
                
                # Append the new email
                # Check if the list is empty or ends with a comma
                if current_list_str.strip():
                    if not current_list_str.strip().rstrip().endswith(','):
                         extension = f',\n    "{new_email}",\n'
                    else:
                         extension = f'\n    "{new_email}",\n'
                else:
                    extension = f'\n    "{new_email}",\n'
                
                replacement = f'{match.group(1)}{current_list_str}{extension}{match.group(3)}'
                new_content = content.replace(match.group(0), replacement)
                
            else:
                 # Legacy replace all logic (kept just in case, though UI won't use it)
                emails = value.split(',')
                formatted_emails = '[\n'
                for email in emails:
                    email = email.strip()
                    if email:
                        formatted_emails += f'    "{email}",\n'
                formatted_emails += ']'
                replacement = f'{key} = {formatted_emails}'
                new_content = re.sub(r'CHARGE_EMAIL_RECIPIENTS\s*=\s*\[.*?\]', replacement, content, flags=re.DOTALL)

        else:
            # Assume number for thresholds
            replacement = f'{key} = {value}'
            pattern = f'{key}\\s*=\\s*[0-9.]+'
            new_content = re.sub(pattern, replacement, content, count=1)

        with open(config_path, 'w') as f:
            f.write(new_content)
            
        print(f"Successfully updated {key}")
        return True

    except Exception as e:
        print(f"Error updating {key}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update configuration values in src/config.py')
    parser.add_argument('--add-email', help='Single email to add to the list')
    parser.add_argument('--alert-threshold', type=float, help='Price threshold for alerts')
    parser.add_argument('--charge-threshold', type=float, help='Price threshold for charging')
    
    args = parser.parse_args()
    
    config_path = Path('src/config.py')
    
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    success = True
    
    if args.add_email:
        if not update_config(config_path, 'CHARGE_EMAIL_RECIPIENTS', args.add_email, append=True):
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
