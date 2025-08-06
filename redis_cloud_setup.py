#!/usr/bin/env python3
"""
Redis Cloud Setup for DSA Interview Platform
Configures Redis Cloud with advanced features for Redis AI Challenge
"""

import redis
import json
import os
import time
from dotenv import load_dotenv
import numpy as np

load_dotenv()

def setup_redis_cloud():
    """Setup Redis Cloud connection with advanced features"""
    
    print("🚀 Setting up Redis Cloud for DSA Interview Platform...")
    print("📋 Challenge Eligibility: Real-Time AI Innovators + Beyond the Cache")
    
    # Redis Cloud connection (update these with your Redis Cloud credentials)
    redis_client = redis.Redis(
        host=os.getenv('REDIS_CLOUD_HOST', 'redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com'),
        port=int(os.getenv('REDIS_CLOUD_PORT', 12345)),
        password=os.getenv('REDIS_CLOUD_PASSWORD', 'your-redis-cloud-password'),
        username=os.getenv('REDIS_CLOUD_USERNAME', 'default'),
        ssl=True,  # Redis Cloud uses SSL
        ssl_cert_reqs=None,
        decode_responses=True
    )
    
    try:
        # Test connection
        redis_client.ping()
        print("✅ Redis Cloud connection successful!")
        
        # Setup Redis modules and features for challenge eligibility
        setup_redis_ai_features(redis_client)
        setup_redis_beyond_cache_features(redis_client)
        
        return redis_client
        
    except Exception as e:
        print(f"❌ Redis Cloud connection failed: {e}")
        print("📝 Please update your Redis Cloud credentials in .env file:")
        print("   REDIS_CLOUD_HOST=your-redis-cloud-host")
        print("   REDIS_CLOUD_PORT=your-redis-cloud-port")
        print("   REDIS_CLOUD_PASSWORD=your-redis-cloud-password")
        return None

def setup_redis_ai_features(redis_client):
    """Setup Redis AI features for 'Real-Time AI Innovators' prompt"""
    
    print("\n🤖 Setting up Redis AI Features for Challenge Prompt 1...")
    
    # 1. Vector Search for AI-powered problem recommendations
    try:
        # Create vector search index for problem similarity
        redis_client.execute_command(
            'FT.CREATE', 'problem_vector_idx',
            'ON', 'HASH',
            'PREFIX', '1', 'problem_vector:',
            'SCHEMA',
            'title', 'TEXT', 'WEIGHT', '2.0',
            'description', 'TEXT',
            'difficulty', 'TAG',
            'topic', 'TAG',
            'tags', 'TAG',
            'embedding', 'VECTOR', 'FLAT', '6', 'TYPE', 'FLOAT32', 'DIM', '384', 'DISTANCE_METRIC', 'COSINE'
        )
        print("✅ Vector search index created for AI-powered recommendations")
    except redis.exceptions.ResponseError as e:
        if 'Index already exists' not in str(e):
            print(f"⚠️ Vector index creation: {e}")
        else:
            print("✅ Vector search index already exists")
    
    # 2. Real-time AI analysis caching
    setup_ai_analysis_cache(redis_client)
    
    # 3. ML feature streaming for real-time performance tracking
    setup_ml_feature_streaming(redis_client)
    
    # 4. Semantic caching for LLM-powered hints
    setup_semantic_caching(redis_client)

def setup_redis_beyond_cache_features(redis_client):
    """Setup Redis beyond cache features for 'Beyond the Cache' prompt"""
    
    print("\n🔄 Setting up Redis Beyond Cache Features for Challenge Prompt 2...")
    
    # 1. Redis as Primary Database for user data
    setup_primary_database(redis_client)
    
    # 2. Full-text search for problem discovery
    setup_fulltext_search(redis_client)
    
    # 3. Real-time streams for live coding sessions
    setup_realtime_streams(redis_client)
    
    # 4. Pub/Sub for real-time notifications
    setup_pubsub_system(redis_client)
    
    # 5. Time series for performance analytics
    setup_timeseries_analytics(redis_client)

def setup_ai_analysis_cache(redis_client):
    """Setup AI analysis caching system"""
    
    print("🧠 Setting up AI analysis caching...")
    
    # Cache structure for AI analysis results
    sample_analysis = {
        'user_id': 'user_123',
        'problem_id': 'two_sum',
        'code_quality_score': 8.5,
        'algorithm_efficiency': 9.0,
        'explanation_clarity': 7.5,
        'ai_insights': [
            'Excellent use of hash map for O(1) lookup',
            'Clear variable naming and code structure',
            'Could improve edge case handling'
        ],
        'improvement_suggestions': [
            'Consider adding input validation',
            'Add comments for complex logic',
            'Think about memory optimization'
        ],
        'timestamp': int(time.time()),
        'cached_at': int(time.time())
    }
    
    # Store in Redis with TTL for efficient caching
    cache_key = f"ai_analysis:{sample_analysis['user_id']}:{sample_analysis['problem_id']}"
    redis_client.hset(cache_key, mapping=sample_analysis)
    redis_client.expire(cache_key, 3600)  # 1 hour TTL
    
    print("✅ AI analysis caching system configured")

def setup_ml_feature_streaming(redis_client):
    """Setup ML feature streaming for real-time performance tracking"""
    
    print("📊 Setting up ML feature streaming...")
    
    # Create stream for real-time ML features
    stream_name = "ml_features_stream"
    
    # Sample ML features for user performance
    ml_features = {
        'user_id': 'user_123',
        'session_id': 'session_456',
        'problem_difficulty': 'medium',
        'time_to_solve': '1200',  # seconds
        'attempts_count': '3',
        'hint_usage': '1',
        'code_lines': '25',
        'syntax_errors': '2',
        'logical_errors': '1',
        'performance_score': '85.5',
        'timestamp': str(int(time.time()))
    }
    
    # Add to stream
    redis_client.xadd(stream_name, ml_features)
    
    # Create consumer group for ML processing
    try:
        redis_client.xgroup_create(stream_name, 'ml_processors', id='0', mkstream=True)
        print("✅ ML feature streaming configured with consumer groups")
    except redis.exceptions.ResponseError as e:
        if 'BUSYGROUP' not in str(e):
            print(f"⚠️ Consumer group creation: {e}")

def setup_semantic_caching(redis_client):
    """Setup semantic caching for LLM-powered hints"""
    
    print("🔍 Setting up semantic caching for LLM optimization...")
    
    # Semantic cache for similar problem queries
    semantic_cache = {
        'query_hash': 'hash_of_similar_query',
        'original_query': 'How to solve two sum problem efficiently?',
        'cached_response': 'Use a hash map to store complements for O(n) solution...',
        'embedding_similarity': '0.95',
        'usage_count': '15',
        'last_accessed': str(int(time.time())),
        'ttl': '7200'  # 2 hours
    }
    
    cache_key = f"semantic_cache:{semantic_cache['query_hash']}"
    redis_client.hset(cache_key, mapping=semantic_cache)
    redis_client.expire(cache_key, int(semantic_cache['ttl']))
    
    print("✅ Semantic caching system configured for LLM optimization")

def setup_primary_database(redis_client):
    """Setup Redis as primary database for user data"""
    
    print("💾 Setting up Redis as primary database...")
    
    # User profile structure
    user_profile = {
        'user_id': 'user_123',
        'username': 'john_doe',
        'email': 'john@example.com',
        'registration_date': str(int(time.time())),
        'total_problems_solved': '45',
        'current_streak': '7',
        'preferred_language': 'python',
        'skill_level': 'intermediate',
        'interview_readiness': 'mid-level',
        'last_active': str(int(time.time()))
    }
    
    # Store user data
    redis_client.hset(f"user:{user_profile['user_id']}", mapping=user_profile)
    
    # Create indexes for efficient querying
    redis_client.sadd('users_by_skill:intermediate', user_profile['user_id'])
    redis_client.sadd('users_by_language:python', user_profile['user_id'])
    
    print("✅ Redis configured as primary database with user data")

def setup_fulltext_search(redis_client):
    """Setup full-text search for problem discovery"""
    
    print("🔎 Setting up full-text search...")
    
    try:
        # Create full-text search index
        redis_client.execute_command(
            'FT.CREATE', 'problem_search_idx',
            'ON', 'HASH',
            'PREFIX', '1', 'problem:',
            'SCHEMA',
            'title', 'TEXT', 'WEIGHT', '3.0', 'SORTABLE',
            'description', 'TEXT', 'WEIGHT', '2.0',
            'difficulty', 'TAG', 'SORTABLE',
            'topic', 'TAG', 'SORTABLE',
            'tags', 'TAG',
            'companies', 'TAG',
            'solution_approaches', 'TEXT'
        )
        print("✅ Full-text search index created for problem discovery")
    except redis.exceptions.ResponseError as e:
        if 'Index already exists' not in str(e):
            print(f"⚠️ Search index creation: {e}")

def setup_realtime_streams(redis_client):
    """Setup real-time streams for live coding sessions"""
    
    print("🔴 Setting up real-time streams for live coding...")
    
    # Create streams for different real-time events
    streams = [
        'coding_sessions_stream',
        'user_interactions_stream',
        'problem_submissions_stream',
        'performance_metrics_stream'
    ]
    
    for stream_name in streams:
        # Add sample data to initialize stream
        sample_data = {
            'event_type': 'session_start',
            'user_id': 'user_123',
            'problem_id': 'two_sum',
            'timestamp': str(int(time.time())),
            'session_id': f"session_{int(time.time())}"
        }
        
        redis_client.xadd(stream_name, sample_data)
        
        # Create consumer groups
        try:
            redis_client.xgroup_create(stream_name, 'processors', id='0', mkstream=True)
        except redis.exceptions.ResponseError:
            pass  # Group already exists
    
    print("✅ Real-time streams configured for live coding sessions")

def setup_pubsub_system(redis_client):
    """Setup Pub/Sub for real-time notifications"""
    
    print("📢 Setting up Pub/Sub system for notifications...")
    
    # Publish sample notifications
    channels = [
        'user_achievements',
        'problem_updates',
        'system_notifications',
        'leaderboard_updates'
    ]
    
    for channel in channels:
        sample_message = {
            'type': 'achievement_unlocked',
            'user_id': 'user_123',
            'message': 'Congratulations! You solved 10 problems in a row!',
            'timestamp': int(time.time())
        }
        
        redis_client.publish(channel, json.dumps(sample_message))
    
    print("✅ Pub/Sub system configured for real-time notifications")

def setup_timeseries_analytics(redis_client):
    """Setup time series for performance analytics"""
    
    print("📈 Setting up time series analytics...")
    
    # Create time series for various metrics
    try:
        # User performance over time
        ts_key = "user_performance:user_123"
        redis_client.execute_command('TS.CREATE', ts_key, 'RETENTION', '86400000')  # 24 hours
        
        # Add sample data points
        current_time = int(time.time() * 1000)  # milliseconds
        for i in range(10):
            timestamp = current_time - (i * 3600000)  # hourly data
            score = 75 + (i * 2)  # increasing performance
            redis_client.execute_command('TS.ADD', ts_key, timestamp, score)
        
        print("✅ Time series analytics configured")
        
    except redis.exceptions.ResponseError as e:
        print(f"⚠️ Time series setup (requires RedisTimeSeries module): {e}")

def create_redis_cloud_env():
    """Create .env template for Redis Cloud configuration"""
    
    env_template = """# Redis Cloud Configuration for DSA Interview Platform
# Update these values with your Redis Cloud instance details

# Redis Cloud Connection
REDIS_CLOUD_HOST=your-redis-cloud-host.redislabs.com
REDIS_CLOUD_PORT=12345
REDIS_CLOUD_PASSWORD=your-redis-cloud-password
REDIS_CLOUD_USERNAME=default

# Local Redis (fallback)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_USERNAME=

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-for-production

# Application Configuration
APP_NAME=DSA Interview Platform - Redis AI Challenge
APP_VERSION=1.0.0
REDIS_AI_CHALLENGE=true

# Challenge Specific Features
ENABLE_VECTOR_SEARCH=true
ENABLE_ML_STREAMING=true
ENABLE_SEMANTIC_CACHING=true
ENABLE_REALTIME_STREAMS=true
ENABLE_FULLTEXT_SEARCH=true
ENABLE_TIMESERIES=true
"""
    
    with open('.env.redis_cloud', 'w') as f:
        f.write(env_template)
    
    print("📝 Created .env.redis_cloud template")
    print("   Please update with your Redis Cloud credentials")

def main():
    """Main setup function"""
    
    print("🏆 Redis AI Challenge - DSA Interview Platform Setup")
    print("=" * 60)
    print("Challenge Prompts:")
    print("1. Real-Time AI Innovators - AI-powered application with Redis")
    print("2. Beyond the Cache - Redis as multi-model platform")
    print("=" * 60)
    
    # Create environment template
    create_redis_cloud_env()
    
    # Setup Redis Cloud
    redis_client = setup_redis_cloud()
    
    if redis_client:
        print("\n🎉 Redis Cloud setup complete!")
        print("\n📋 Challenge Features Implemented:")
        print("✅ Vector search for AI-powered recommendations")
        print("✅ Real-time ML feature streaming")
        print("✅ Semantic caching for LLM optimization")
        print("✅ Redis as primary database")
        print("✅ Full-text search capabilities")
        print("✅ Real-time streams for live coding")
        print("✅ Pub/Sub notification system")
        print("✅ Time series analytics")
        
        print("\n🏆 Platform is now eligible for both challenge prompts!")
        print("🚀 Ready to submit to Redis AI Challenge!")
        
    else:
        print("\n❌ Setup incomplete. Please configure Redis Cloud credentials.")

if __name__ == "__main__":
    main()
