#!/usr/bin/env bash
# Exit immediately if any command exits with a non-zero status
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate
