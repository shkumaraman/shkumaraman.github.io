#!/bin/bash

# Install all dependencies
pip install -r requirements.txt

# Install Playwright dependencies (including browser binaries)
python -m playwright install --with-deps
