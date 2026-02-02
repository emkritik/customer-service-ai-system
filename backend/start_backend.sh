#!/bin/bash
# Startup script for the Customer Service Support System backend

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY environment variable is not set"
    echo ""
    echo "Please set your API key first:"
    echo "  export ANTHROPIC_API_KEY=\"your-api-key-here\""
    echo ""
    echo "Or create a .env file with your key (not tracked by git)"
    exit 1
fi

# Navigate to the backend directory
cd "$(dirname "$0")"

# Start the uvicorn server
echo "Starting Customer Service Support System backend..."
echo "API URL: http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

uvicorn api.main:app --reload --port 8000
