#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install it first."
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the Linux version of the application
python3 linux_app.py