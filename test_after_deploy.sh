#!/bin/bash

echo "Waiting 2 minutes for Render to deploy..."
echo "Meanwhile, check: https://dashboard.render.com"
echo ""
echo "Press ENTER when you see 'Deploy live' in Render..."
read

echo "Testing backend..."
python test_backend_slow.py
