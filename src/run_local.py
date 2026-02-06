"""
Local Runner
Runs the price monitor in a loop for local testing.
Loads configuration from .env file.
"""

import time
import os
from pathlib import Path
from dotenv import load_dotenv
from main import main

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

if __name__ == "__main__":
    print("🚀 Starting Local Price Monitor")
    print(f"Loaded configuration from {env_path}")
    print("Press Ctrl+C to stop")
    print("-" * 40)
    
    # Check if we need to warn about missing config
    required_vars = ["GMAIL_USER", "GMAIL_APP_PASSWORD", "PHONE_NUMBER"]
    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing)}")
        print("   SMS notifications will NOT work.")
        print("   Please create a .env file with your credentials.")
        print("-" * 40)
        time.sleep(2)

    try:
        while True:
            try:
                main()
            except Exception as e:
                print(f"Error in main loop: {e}")
            
            # Wait for 5 minutes
            print("Sleeping for 5 minutes...\n")
            time.sleep(300)
            
    except KeyboardInterrupt:
        print("\nStopping monitor...")
