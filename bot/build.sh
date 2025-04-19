#!/bin/bash

# Install all required dependencies
pip install -r requirements.txt

# Install Playwright and its required binaries (browsers)
python -m playwright install
