#!/bin/bash

# Configuration
SERVICE_NAME="com.github.ashraf8ila.tesla-comed"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_DIR="$HOME/.tesla-comed-runtime"
PLIST_PATH="$HOME/Library/LaunchAgents/$SERVICE_NAME.plist"
LOG_DIR="$HOME/Library/Logs/$SERVICE_NAME"
# Note: Using standard user log directory

# Ensure directories exist
mkdir -p "$LOG_DIR"
mkdir -p "$RUNTIME_DIR"

# Deploy Code to Runtime Directory (to bypass TCC restrictions on Documents)
echo "Deploying code to $RUNTIME_DIR..."
rm -rf "$RUNTIME_DIR/src"
cp -r "$PROJECT_DIR/src" "$RUNTIME_DIR/"
# Copy state if it exists, otherwise it will be created
if [ -f "$PROJECT_DIR/state.json" ]; then
    cp "$PROJECT_DIR/state.json" "$RUNTIME_DIR/"
fi

echo "Installing service $SERVICE_NAME..."
echo "Runtime Dir: $RUNTIME_DIR"

# Generate Plist
cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$SERVICE_NAME</string>

    <key>ProgramArguments</key>
    <array>
        <string>/Library/Developer/CommandLineTools/usr/bin/python3</string>
        <string>$RUNTIME_DIR/src/main.py</string>
    </array>

    <key>StandardOutPath</key>
    <string>$LOG_DIR/stdout.log</string>

    <key>StandardErrorPath</key>
    <string>$LOG_DIR/stderr.log</string>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

echo "Created plist at $PLIST_PATH"

# Unload existing service (suppress error if not loaded)
if launchctl list | grep -q "$SERVICE_NAME"; then
    echo "Unloading existing service..."
    launchctl unload "$PLIST_PATH"
fi

# Load new service
echo "Loading new service..."
launchctl load "$PLIST_PATH"

echo "✅ Service installed and started!"
echo "Logs are located at: $LOG_DIR"
echo "You can check status with: launchctl list | grep $SERVICE_NAME"
