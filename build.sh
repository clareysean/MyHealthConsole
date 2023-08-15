#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install dependencies, including gunicorn
pip install -r requirements.txt

# Run Gunicorn with your Django application
gunicorn healthapp.wsgi

