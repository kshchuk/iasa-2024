#!/bin/bash

# Create a Python virtual environment
python -m venv venv || { echo "Failed to create virtual environment"; exit 1; }

# Activate the virtual environment
source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install required packages
pip install -r requirements.txt || { echo "Failed to install required packages in unix_requirements.txt"; exit 1; }

echo "Setup completed successfully"