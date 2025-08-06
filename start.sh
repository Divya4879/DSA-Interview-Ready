#!/bin/bash

# Quick Start Script for Redis AI Challenge Platform
echo "🏆 Starting Redis AI Challenge Platform..."

# Check if we're in the right directory
if [ ! -f "app_redis_cloud.py" ]; then
    echo "❌ Please run from the dsa-interview directory"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run ./deploy_local_complete.sh first"
    exit 1
fi

# Quick Redis test
python3 -c "
from app_redis_cloud import get_redis_client
try:
    redis_client = get_redis_client()
    redis_client.ping()
    print('✅ Redis Cloud connected')
except:
    print('❌ Redis Cloud connection failed')
    exit(1)
" || exit 1

# Start the platform
echo ""
echo "🌐 Starting at: http://localhost:5000"
echo "🏆 Redis AI Challenge features active"
echo "Press Ctrl+C to stop"
echo ""

python3 run_platform.py
