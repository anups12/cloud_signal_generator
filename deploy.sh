#!/bin/bash

echo "🚀 Starting Flask Signal Broadcaster..."

# Activate existing virtual environment
source venv/bin/activate

# Export environment variables from .env file
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Environment variables loaded."
else
  echo "⚠️  .env file not found! Please create and configure your .env file."
  exit 1
fi

# Run Gunicorn server with Eventlet worker
echo "🚀 Running Flask app with Gunicorn..."
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:60020 run:app
