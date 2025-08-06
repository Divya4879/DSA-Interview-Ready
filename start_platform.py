#!/usr/bin/env python3
"""
Start the Redis AI Challenge Platform with proper error handling
"""

import os
import sys
from dotenv import load_dotenv

def test_redis_connection():
    """Test Redis connection before starting the app"""
    try:
        from app_redis_cloud import get_redis_client
        
        print("🔍 Testing Redis Cloud connection...")
        redis_client = get_redis_client()
        redis_client.ping()
        print("✅ Redis Cloud connection successful!")
        
        # Check if data exists
        problems = redis_client.smembers('all_problems')
        users = redis_client.keys('user:*')
        
        print(f"✅ Found {len(problems)} problems")
        print(f"✅ Found {len(users)} users")
        
        if len(problems) == 0:
            print("⚠️  No problems found. Running initialization...")
            os.system("python3 init_redis_cloud_compatible.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if your Redis Cloud instance is running")
        print("2. Verify credentials in .env file")
        print("3. Run: python3 quick_redis_test.py")
        return False

def start_flask_app():
    """Start the Flask application"""
    try:
        print("\n🚀 Starting Redis AI Challenge Platform...")
        print("🌐 Platform will be available at: http://localhost:5000")
        print("🏆 Features: AI Recommendations, ML Streaming, Semantic Caching")
        print("📊 Redis Beyond Cache: Primary DB, Time Series, Streams, Pub/Sub")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Import and run the Flask app
        from app_redis_cloud import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Flask app failed to start: {e}")

def main():
    """Main function"""
    print("🏆 Redis AI Challenge - DSA Interview Platform")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Test Redis connection first
    if not test_redis_connection():
        print("\n❌ Cannot start platform without Redis connection")
        sys.exit(1)
    
    # Start Flask app
    start_flask_app()

if __name__ == "__main__":
    main()
