#!/usr/bin/env python3
"""
Redis Cloud Setup Script for DSA Interview Platform
This script helps configure Redis Cloud for production deployment
"""

import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

def test_redis_connection(host, port, password, username=None):
    """Test Redis connection with given credentials"""
    try:
        if username:
            client = redis.Redis(
                host=host,
                port=port,
                username=username,
                password=password,
                decode_responses=True,
                ssl=True,
                ssl_cert_reqs=None
            )
        else:
            client = redis.Redis(
                host=host,
                port=port,
                password=password,
                decode_responses=True,
                ssl=True,
                ssl_cert_reqs=None
            )
        
        # Test connection
        client.ping()
        print(f"✅ Successfully connected to Redis Cloud!")
        
        # Test basic operations
        client.set("test_key", "test_value")
        value = client.get("test_key")
        client.delete("test_key")
        
        print(f"✅ Basic operations working!")
        return client
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def setup_redis_cloud_env():
    """Generate environment variables for Redis Cloud"""
    print("""
🚀 Redis Cloud Setup Instructions:

1. Go to https://redis.com/try-free/
2. Sign up for a free Redis Cloud account
3. Create a new database with these settings:
   - Cloud Provider: AWS/GCP (your choice)
   - Region: Choose closest to your users
   - Redis Version: 7.2+ (with modules)
   - Memory: 30MB (free tier)
   - Modules: Enable RedisJSON, RediSearch, RedisTimeSeries

4. After creation, get your connection details:
   - Endpoint (host:port)
   - Password
   - Username (if required)

5. Update your .env file with these values:
""")
    
    print("""
# Redis Cloud Configuration (Production)
REDIS_CLOUD_HOST=your-redis-endpoint.redis.cloud
REDIS_CLOUD_PORT=12345
REDIS_CLOUD_PASSWORD=your-redis-password
REDIS_CLOUD_USERNAME=default  # Optional

# For production, use Redis Cloud
REDIS_HOST=${REDIS_CLOUD_HOST}
REDIS_PORT=${REDIS_CLOUD_PORT}
REDIS_PASSWORD=${REDIS_CLOUD_PASSWORD}
""")

def migrate_data_to_cloud(local_client, cloud_client):
    """Migrate data from local Redis to Redis Cloud"""
    print("🔄 Starting data migration...")
    
    # Get all problem keys
    problem_keys = local_client.keys("problem:*")
    print(f"📊 Found {len(problem_keys)} problems to migrate")
    
    # Migrate problems
    for i, key in enumerate(problem_keys):
        data = local_client.hgetall(key)
        cloud_client.hset(key, mapping=data)
        
        if (i + 1) % 100 == 0:
            print(f"✅ Migrated {i + 1} problems...")
    
    # Migrate indexes
    for difficulty in ['easy', 'medium', 'hard']:
        for topic in ['arrays', 'strings', 'trees', 'graphs', 'dynamic-programming']:
            key = f"problems:{difficulty}:{topic}"
            if local_client.exists(key):
                members = local_client.zrange(key, 0, -1, withscores=True)
                if members:
                    cloud_client.zadd(key, dict(members))
    
    # Migrate sets
    for set_key in ['topics', 'difficulties', 'companies']:
        if local_client.exists(set_key):
            members = local_client.smembers(set_key)
            if members:
                cloud_client.sadd(set_key, *members)
    
    # Migrate stats
    if local_client.exists('platform_stats'):
        stats = local_client.hgetall('platform_stats')
        cloud_client.hset('platform_stats', mapping=stats)
    
    print("✅ Data migration completed!")

def setup_redis_ai_features(client):
    """Setup Redis AI features for the platform"""
    print("🤖 Setting up Redis AI features...")
    
    # Create vector index for problem similarity
    try:
        # Check if index exists
        try:
            client.execute_command("FT.INFO", "problem_vectors")
            print("✅ Vector index already exists")
        except:
            # Create vector index for problem similarity
            client.execute_command(
                "FT.CREATE", "problem_vectors",
                "ON", "HASH",
                "PREFIX", "1", "problem_vector:",
                "SCHEMA",
                "problem_id", "TEXT",
                "title", "TEXT",
                "description", "TEXT",
                "topic", "TAG",
                "difficulty", "TAG",
                "embedding", "VECTOR", "FLAT", "6", "TYPE", "FLOAT32", "DIM", "384", "DISTANCE_METRIC", "COSINE"
            )
            print("✅ Created vector index for problem similarity")
    except Exception as e:
        print(f"⚠️ Vector index setup failed: {e}")
    
    # Setup time series for analytics
    try:
        # User activity time series
        client.execute_command("TS.CREATE", "user_activity", "RETENTION", "86400000")  # 24 hours
        client.execute_command("TS.CREATE", "problem_submissions", "RETENTION", "86400000")
        client.execute_command("TS.CREATE", "ai_analysis_requests", "RETENTION", "86400000")
        print("✅ Created time series for analytics")
    except Exception as e:
        print(f"⚠️ Time series setup failed: {e}")

def test_redis_cloud_setup():
    """Test Redis Cloud setup with sample credentials"""
    print("🧪 Testing Redis Cloud connection...")
    
    # Sample connection test
    host = input("Enter Redis Cloud host (e.g., redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com): ").strip()
    port = input("Enter Redis Cloud port (e.g., 12345): ").strip()
    password = input("Enter Redis Cloud password: ").strip()
    username = input("Enter Redis Cloud username (press Enter if none): ").strip()
    
    if not username:
        username = None
    
    try:
        port = int(port)
    except:
        print("❌ Invalid port number")
        return
    
    client = test_redis_connection(host, port, password, username)
    
    if client:
        print("\n🎉 Redis Cloud connection successful!")
        
        # Test AI features
        setup_redis_ai_features(client)
        
        # Generate .env configuration
        print(f"""
📝 Add these to your .env file:

REDIS_CLOUD_HOST={host}
REDIS_CLOUD_PORT={port}
REDIS_CLOUD_PASSWORD={password}
""")
        if username:
            print(f"REDIS_CLOUD_USERNAME={username}")
        
        print("""
# For production deployment
REDIS_HOST=${REDIS_CLOUD_HOST}
REDIS_PORT=${REDIS_CLOUD_PORT}
REDIS_PASSWORD=${REDIS_CLOUD_PASSWORD}
""")

if __name__ == "__main__":
    print("🔧 Redis Cloud Setup for DSA Interview Platform")
    print("=" * 50)
    
    choice = input("""
Choose an option:
1. Show Redis Cloud setup instructions
2. Test Redis Cloud connection
3. Migrate local data to Redis Cloud
4. Setup Redis AI features

Enter choice (1-4): """).strip()
    
    if choice == "1":
        setup_redis_cloud_env()
    elif choice == "2":
        test_redis_cloud_setup()
    elif choice == "3":
        print("Data migration requires both local and cloud Redis connections")
        # Implementation for data migration
    elif choice == "4":
        print("Setting up Redis AI features on current connection...")
        local_client = redis.Redis(decode_responses=True)
        setup_redis_ai_features(local_client)
    else:
        print("Invalid choice")
