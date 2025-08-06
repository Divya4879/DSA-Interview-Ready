#!/usr/bin/env python3
"""
Initialize Redis Cloud with AI Challenge data and indexes
"""

import redis
import json
import os
import time
from dotenv import load_dotenv

def connect_redis_cloud():
    """Connect to Redis Cloud with SSL"""
    load_dotenv()
    
    try:
        # Redis Cloud connection with SSL
        redis_client = redis.Redis(
            host=os.getenv('REDIS_CLOUD_HOST'),
            port=int(os.getenv('REDIS_CLOUD_PORT')),
            password=os.getenv('REDIS_CLOUD_PASSWORD'),
            username=os.getenv('REDIS_CLOUD_USERNAME', 'default'),
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,
            socket_timeout=30,
            socket_connect_timeout=30
        )
        
        # Test connection
        redis_client.ping()
        print("✅ Connected to Redis Cloud successfully!")
        return redis_client
        
    except Exception as e:
        print(f"❌ Redis Cloud connection failed: {e}")
        return None

def create_search_indexes(redis_client):
    """Create search indexes for AI Challenge features"""
    
    print("🔍 Creating search indexes...")
    
    # 1. Problem search index (Beyond the Cache - Full-text search)
    try:
        redis_client.execute_command(
            'FT.CREATE', 'problem_search_idx',
            'ON', 'HASH',
            'PREFIX', '1', 'problem:',
            'SCHEMA',
            'title', 'TEXT', 'WEIGHT', '3.0', 'SORTABLE',
            'description', 'TEXT', 'WEIGHT', '2.0',
            'difficulty', 'TAG', 'SORTABLE',
            'topic', 'TAG', 'SORTABLE',
            'tags', 'TAG'
        )
        print("✅ Problem search index created")
    except redis.exceptions.ResponseError as e:
        if 'Index already exists' in str(e):
            print("✅ Problem search index already exists")
        else:
            print(f"⚠️ Problem search index error: {e}")
    
    # 2. Vector search index (Real-Time AI - Vector recommendations)
    try:
        redis_client.execute_command(
            'FT.CREATE', 'problem_vector_idx',
            'ON', 'HASH',
            'PREFIX', '1', 'problem_vector:',
            'SCHEMA',
            'title', 'TEXT', 'WEIGHT', '2.0',
            'description', 'TEXT',
            'difficulty', 'TAG',
            'topic', 'TAG',
            'embedding', 'VECTOR', 'FLAT', '6', 'TYPE', 'FLOAT32', 'DIM', '128', 'DISTANCE_METRIC', 'COSINE'
        )
        print("✅ Vector search index created")
    except redis.exceptions.ResponseError as e:
        if 'Index already exists' in str(e):
            print("✅ Vector search index already exists")
        else:
            print(f"⚠️ Vector search index error: {e}")

def create_sample_problems(redis_client):
    """Create sample problems for the AI Challenge"""
    
    print("📚 Creating sample problems...")
    
    problems = [
        {
            'id': 'two_sum_ai',
            'title': 'Two Sum - AI Enhanced',
            'description': 'Find two numbers in array that add up to target. Enhanced with AI recommendations.',
            'difficulty': 'easy',
            'topic': 'arrays',
            'tags': json.dumps(['Array', 'Hash Table', 'AI-Enhanced']),
            'examples': json.dumps([
                {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'AI suggests hash table approach for O(n) solution'}
            ]),
            'hints': json.dumps(['Use hash table for O(1) lookup', 'AI recommends this pattern for similar problems']),
            'constraints': json.dumps(['2 ≤ nums.length ≤ 10⁴', 'AI optimized for large inputs'])
        },
        {
            'id': 'design_twitter_ai',
            'title': 'Design Twitter - Redis Powered',
            'description': 'Design Twitter using Redis as the backend. Showcases Redis beyond cache capabilities.',
            'difficulty': 'medium',
            'topic': 'design',
            'tags': json.dumps(['Design', 'Redis', 'Real-time', 'Streams']),
            'examples': json.dumps([
                {'input': 'postTweet(1, 5)', 'output': 'null', 'explanation': 'Uses Redis Streams for real-time updates'}
            ]),
            'hints': json.dumps(['Use Redis Streams for timeline', 'Redis Sorted Sets for followers', 'Redis Pub/Sub for notifications']),
            'constraints': json.dumps(['1 ≤ userId ≤ 500', 'Redis handles millions of operations/sec'])
        },
        {
            'id': 'ml_recommendation_system',
            'title': 'ML Recommendation System',
            'description': 'Build a recommendation system using Redis vector search and real-time ML features.',
            'difficulty': 'hard',
            'topic': 'machine-learning',
            'tags': json.dumps(['ML', 'Vector Search', 'Real-time', 'AI']),
            'examples': json.dumps([
                {'input': 'user_preferences = [0.1, 0.8, 0.3]', 'output': 'recommended_items', 'explanation': 'Uses Redis vector search for similarity matching'}
            ]),
            'hints': json.dumps(['Use Redis vector search', 'Stream ML features in real-time', 'Cache embeddings for performance']),
            'constraints': json.dumps(['Vector dimension ≤ 512', 'Real-time processing < 100ms'])
        }
    ]
    
    for problem in problems:
        # Store main problem data
        redis_client.hset(f"problem:{problem['id']}", mapping=problem)
        
        # Create vector embedding (simplified for demo)
        import random
        vector_data = {
            'title': problem['title'],
            'description': problem['description'],
            'difficulty': problem['difficulty'],
            'topic': problem['topic'],
            'embedding': ','.join([str(random.random()) for _ in range(128)])  # 128-dim vector
        }
        redis_client.hset(f"problem_vector:{problem['id']}", mapping=vector_data)
        
        # Add to topic sets
        redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
        redis_client.sadd('topics', problem['topic'])
        redis_client.sadd('difficulties', problem['difficulty'])
        
        print(f"✅ Created problem: {problem['title']}")

def setup_ai_features(redis_client):
    """Setup AI Challenge specific features"""
    
    print("🤖 Setting up AI Challenge features...")
    
    # 1. ML Feature Streaming (Real-Time AI Innovators)
    stream_name = "ml_features_stream"
    sample_ml_data = {
        'user_id': 'demo_user',
        'problem_id': 'two_sum_ai',
        'session_id': f'session_{int(time.time())}',
        'time_spent': '300',
        'code_quality_score': '85',
        'ai_recommendation_used': 'true',
        'timestamp': str(int(time.time()))
    }
    
    try:
        redis_client.xadd(stream_name, sample_ml_data)
        redis_client.xgroup_create(stream_name, 'ai_processors', id='0', mkstream=True)
        print("✅ ML feature streaming configured")
    except redis.exceptions.ResponseError as e:
        if 'BUSYGROUP' not in str(e):
            print(f"⚠️ ML streaming setup: {e}")
    
    # 2. Semantic Caching (LLM Optimization)
    semantic_cache_data = {
        'query_hash': 'demo_query_hash',
        'original_query': 'How to solve two sum efficiently?',
        'cached_response': 'Use hash table for O(n) time complexity. Store complements as you iterate.',
        'similarity_score': '0.95',
        'usage_count': '1',
        'created_at': str(int(time.time()))
    }
    
    redis_client.hset('semantic_cache:demo_query_hash', mapping=semantic_cache_data)
    redis_client.expire('semantic_cache:demo_query_hash', 7200)  # 2 hours TTL
    print("✅ Semantic caching configured")
    
    # 3. Time Series Analytics (Beyond the Cache)
    try:
        ts_key = "user_performance:demo_user"
        redis_client.execute_command('TS.CREATE', ts_key, 'RETENTION', '86400000')  # 24 hours
        
        # Add sample performance data
        current_time = int(time.time() * 1000)
        for i in range(10):
            timestamp = current_time - (i * 3600000)  # hourly data
            score = 70 + (i * 3)  # improving performance
            redis_client.execute_command('TS.ADD', ts_key, timestamp, score)
        
        print("✅ Time series analytics configured")
    except redis.exceptions.ResponseError as e:
        print(f"⚠️ Time series setup: {e}")
    
    # 4. Real-time Streams (Beyond the Cache)
    coding_session_data = {
        'event_type': 'session_start',
        'user_id': 'demo_user',
        'problem_id': 'two_sum_ai',
        'session_id': f'session_{int(time.time())}',
        'timestamp': str(int(time.time()))
    }
    
    redis_client.xadd('coding_sessions_stream', coding_session_data)
    print("✅ Real-time streams configured")
    
    # 5. Pub/Sub Notifications (Beyond the Cache)
    notification = {
        'type': 'achievement',
        'user_id': 'demo_user',
        'message': 'Welcome to Redis AI Challenge!',
        'timestamp': int(time.time())
    }
    
    redis_client.publish('user_notifications', json.dumps(notification))
    print("✅ Pub/Sub notifications configured")

def setup_primary_database(redis_client):
    """Setup Redis as primary database (Beyond the Cache)"""
    
    print("💾 Setting up Redis as primary database...")
    
    # User profiles
    users = [
        {
            'user_id': 'demo_user',
            'username': 'ai_challenger',
            'email': 'challenger@redis.ai',
            'skill_level': 'intermediate',
            'problems_solved': '15',
            'current_streak': '5',
            'preferred_language': 'python',
            'registration_date': str(int(time.time())),
            'total_session_time': '7200',
            'average_score': '82.5'
        },
        {
            'user_id': 'expert_user',
            'username': 'redis_expert',
            'email': 'expert@redis.ai',
            'skill_level': 'advanced',
            'problems_solved': '50',
            'current_streak': '12',
            'preferred_language': 'python',
            'registration_date': str(int(time.time()) - 86400),
            'total_session_time': '18000',
            'average_score': '91.2'
        }
    ]
    
    for user in users:
        # Store user profile
        redis_client.hset(f"user:{user['user_id']}", mapping=user)
        
        # Create indexes for efficient querying
        redis_client.sadd(f"users_by_skill:{user['skill_level']}", user['user_id'])
        redis_client.sadd(f"users_by_language:{user['preferred_language']}", user['user_id'])
        
        # Add to leaderboard
        redis_client.zadd('global_leaderboard', {user['user_id']: float(user['average_score'])})
        
        print(f"✅ Created user profile: {user['username']}")

def verify_setup(redis_client):
    """Verify all AI Challenge features are working"""
    
    print("\n🔍 Verifying Redis AI Challenge setup...")
    
    # Test search indexes
    try:
        result = redis_client.execute_command('FT.SEARCH', 'problem_search_idx', '*', 'LIMIT', '0', '1')
        print(f"✅ Problem search working - found {result[0]} problems")
    except Exception as e:
        print(f"❌ Problem search test failed: {e}")
    
    # Test vector search
    try:
        result = redis_client.execute_command('FT.SEARCH', 'problem_vector_idx', '*', 'LIMIT', '0', '1')
        print(f"✅ Vector search working - found {result[0]} vectors")
    except Exception as e:
        print(f"❌ Vector search test failed: {e}")
    
    # Test streams
    try:
        result = redis_client.xlen('ml_features_stream')
        print(f"✅ ML streaming working - {result} events in stream")
    except Exception as e:
        print(f"❌ ML streaming test failed: {e}")
    
    # Test time series
    try:
        result = redis_client.execute_command('TS.RANGE', 'user_performance:demo_user', '-', '+')
        print(f"✅ Time series working - {len(result)} data points")
    except Exception as e:
        print(f"❌ Time series test failed: {e}")
    
    # Test primary database
    try:
        user_count = len(redis_client.keys('user:*'))
        print(f"✅ Primary database working - {user_count} users stored")
    except Exception as e:
        print(f"❌ Primary database test failed: {e}")
    
    print("\n🎉 Redis AI Challenge setup verification complete!")

def main():
    """Main setup function"""
    
    print("🏆 Redis AI Challenge - Cloud Initialization")
    print("=" * 50)
    
    # Connect to Redis Cloud
    redis_client = connect_redis_cloud()
    if not redis_client:
        print("❌ Cannot proceed without Redis Cloud connection")
        return
    
    # Setup all features
    create_search_indexes(redis_client)
    create_sample_problems(redis_client)
    setup_ai_features(redis_client)
    setup_primary_database(redis_client)
    verify_setup(redis_client)
    
    print("\n🎉 Redis Cloud initialization complete!")
    print("🚀 Your platform is ready for the Redis AI Challenge!")
    print("\nNext steps:")
    print("1. Run: python3 app_redis_cloud.py")
    print("2. Visit: http://localhost:5000")
    print("3. Test AI features and Redis capabilities")

if __name__ == "__main__":
    main()
