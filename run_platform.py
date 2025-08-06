#!/usr/bin/env python3
"""
Run the Redis AI Challenge Platform with proper error handling
"""

import os
import sys
from dotenv import load_dotenv

def main():
    """Main function to run the platform"""
    print("🏆 Redis AI Challenge - DSA Interview Platform")
    print("=" * 50)
    print("🚀 Features: AI Recommendations, ML Streaming, Semantic Caching")
    print("📊 Redis Beyond Cache: Primary DB, Time Series, Streams, Pub/Sub")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Test Redis connection
    try:
        from app_redis_cloud import get_redis_client
        redis_client = get_redis_client()
        redis_client.ping()
        print("✅ Redis Cloud connection successful")
        
        # Check data
        problems = redis_client.smembers('all_problems')
        print(f"✅ Found {len(problems)} AI Challenge problems")
        
    except Exception as e:
        print(f"⚠️  Redis connection issue: {e}")
        print("Platform will still work with limited functionality")
    
    # Start Flask app
    try:
        print("\n🌐 Starting server at: http://localhost:5000")
        print("🎯 Challenge Features:")
        print("   • AI-powered problem recommendations")
        print("   • Real-time ML feature streaming")
        print("   • Semantic caching for LLM optimization")
        print("   • Redis as primary database")
        print("   • Time series analytics")
        print("   • Real-time streams and Pub/Sub")
        print("\nPress Ctrl+C to stop the server\n")
        
        from app_redis_cloud import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
