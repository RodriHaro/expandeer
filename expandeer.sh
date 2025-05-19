#!/bin/bash
# Launcher for Expandeer

cd /opt/expandeer

# Activate virtual environment if exists
if [ -f "/opt/expandeer/venv/bin/activate" ]; then
    source "/opt/expandeer/venv/bin/activate"
fi

# Run the main app
python3 linux_app.py
