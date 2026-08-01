#!/bin/bash

# Add the backend directory to Python path
export PYTHONPATH="${PYTHONPATH}:./backend"

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 10000
