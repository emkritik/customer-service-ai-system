#!/bin/bash
# Startup script for the Customer Service Support System backend

# Navigate to the backend directory
cd "$(dirname "$0")"

# Load .env file if it exists
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY environment variable is not set"
    echo ""
    echo "Please set your API key first:"
    echo "  export ANTHROPIC_API_KEY=\"your-api-key-here\""
    echo ""
    echo "Or create a .env file with your key (not tracked by git)"
    echo "Example: cp .env.example .env and edit it"
    exit 1
fi

# Start the uvicorn server
echo "Starting Customer Service Support System backend..."
echo "API URL: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

uvicorn api.main:app --reload --port 8000
