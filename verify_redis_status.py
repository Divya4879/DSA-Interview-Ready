#!/usr/bin/env python3
"""
Comprehensive Redis Cloud Status Verification
"""

import redis
import os
import sys
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and has Redis Cloud credentials"""
    print("🔍 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    load_dotenv()
    
    required_vars = ['REDIS_CLOUD_HOST', 'REDIS_CLOUD_PORT', 'REDIS_CLOUD_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your-') or value == 'redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com':
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {value[:20]}..." if len(value) > 20 else f"✅ {var}: {value}")
    
    if missing_vars:
        print(f"❌ Missing or placeholder values for: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def test_redis_cloud_connection():
    """Test Redis Cloud connection with detailed error reporting"""
    print("\n🔗 Testing Redis Cloud connection...")
    
    load_dotenv()
    
    host = os.getenv('REDIS_CLOUD_HOST')
    port = int(os.getenv('REDIS_CLOUD_PORT', 6379))
    password = os.getenv('REDIS_CLOUD_PASSWORD')
    username = os.getenv('REDIS_CLOUD_USERNAME', 'default')
    
    print(f"Connecting to: {host}:{port}")
    
    try:
        # Try Redis Cloud connection with SSL
        redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            username=username,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,
            socket_timeout=10,
            socket_connect_timeout=10
        )
        
        # Test basic connection
        response = redis_client.ping()
        print(f"✅ Redis Cloud connection successful: {response}")
        
        return redis_client
        
    except redis.exceptions.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Check your username and password")
        return None
        
    except redis.exceptions.ConnectionError as e:
        print(f"❌ Connection failed: {e}")
        print("   Check your host and port")
        return None
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_local_redis_fallback():
    """Test local Redis as fallback"""
    print("\n🔄 Testing local Redis fallback...")
    
    try:
        redis_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True,
            socket_timeout=5
        )
        
        response = redis_client.ping()
        print(f"✅ Local Redis connection successful: {response}")
        return redis_client
        
    except Exception as e:
        print(f"❌ Local Redis connection failed: {e}")
        return None

def check_redis_modules(redis_client):
    """Check if required Redis modules are available"""
    print("\n🔧 Checking Redis modules...")
    
    try:
        # Get module list
        modules = redis_client.execute_command('MODULE', 'LIST')
        
        available_modules = []
        for i in range(0, len(modules), 2):
            if i + 1 < len(modules):
                module_info = modules[i + 1]
                if isinstance(module_info, list) and len(module_info) >= 2:
                    module_name = module_info[1]
                    available_modules.append(module_name.lower())
        
        print(f"Available modules: {available_modules}")
        
        # Check required modules
        required_modules = ['search', 'timeseries']
        missing_modules = []
        
        for module in required_modules:
            if any(module in available_module for available_module in available_modules):
                print(f"✅ {module.title()} module available")
            else:
                print(f"❌ {module.title()} module missing")
                missing_modules.append(module)
        
        if missing_modules:
            print(f"\n⚠️  Missing modules: {missing_modules}")
            print("   These are required for AI Challenge features")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking modules: {e}")
        return False

def test_basic_operations(redis_client):
    """Test basic Redis operations"""
    print("\n🧪 Testing basic Redis operations...")
    
    try:
        # Test SET/GET
        redis_client.set('test_key', 'test_value')
        value = redis_client.get('test_key')
        if value == 'test_value':
            print("✅ SET/GET operations working")
        else:
            print("❌ SET/GET operations failed")
            return False
        
        # Test HASH operations
        redis_client.hset('test_hash', 'field1', 'value1')
        hash_value = redis_client.hget('test_hash', 'field1')
        if hash_value == 'value1':
            print("✅ HASH operations working")
        else:
            print("❌ HASH operations failed")
            return False
        
        # Clean up test data
        redis_client.delete('test_key', 'test_hash')
        print("✅ Basic operations test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic operations test failed: {e}")
        return False

def check_existing_data(redis_client):
    """Check if AI Challenge data already exists"""
    print("\n📊 Checking existing AI Challenge data...")
    
    try:
        # Check for problems
        problem_keys = redis_client.keys('problem:*')
        print(f"Found {len(problem_keys)} problems")
        
        # Check for search indexes
        try:
            indexes = redis_client.execute_command('FT._LIST')
            print(f"Found {len(indexes)} search indexes: {indexes}")
        except:
            print("No search indexes found")
        
        # Check for streams
        try:
            stream_length = redis_client.xlen('ml_features_stream')
            print(f"ML features stream has {stream_length} entries")
        except:
            print("ML features stream not found")
        
        # Check for users
        user_keys = redis_client.keys('user:*')
        print(f"Found {len(user_keys)} users")
        
        if len(problem_keys) > 0 or len(user_keys) > 0:
            print("✅ Some AI Challenge data exists")
            return True
        else:
            print("⚠️  No AI Challenge data found - needs initialization")
            return False
            
    except Exception as e:
        print(f"❌ Error checking existing data: {e}")
        return False

def provide_setup_guidance():
    """Provide guidance on next steps"""
    print("\n📋 Setup Guidance:")
    print("=" * 50)
    
    if not check_env_file():
        print("\n🔧 NEXT STEPS:")
        print("1. Create Redis Cloud account at: https://redis.com/try-free/")
        print("2. Create database with RedisSearch and RedisTimeSeries modules")
        print("3. Run: ./test_redis_connection.sh")
        print("4. This will help you configure your .env file")
        return
    
    redis_client = test_redis_cloud_connection()
    
    if not redis_client:
        print("\n🔧 REDIS CLOUD CONNECTION FAILED:")
        print("1. Verify your Redis Cloud credentials")
        print("2. Check if your Redis Cloud instance is running")
        print("3. Ensure SSL/TLS is properly configured")
        print("4. Try running: ./test_redis_connection.sh")
        
        # Try local Redis as fallback
        local_redis = test_local_redis_fallback()
        if local_redis:
            print("\n✅ Local Redis is available as fallback")
            redis_client = local_redis
        else:
            print("\n❌ No Redis connection available")
            return
    
    if redis_client:
        modules_ok = check_redis_modules(redis_client)
        operations_ok = test_basic_operations(redis_client)
        data_exists = check_existing_data(redis_client)
        
        print(f"\n📊 REDIS STATUS SUMMARY:")
        print(f"Connection: {'✅ Working' if redis_client else '❌ Failed'}")
        print(f"Modules: {'✅ Available' if modules_ok else '❌ Missing'}")
        print(f"Operations: {'✅ Working' if operations_ok else '❌ Failed'}")
        print(f"AI Data: {'✅ Exists' if data_exists else '⚠️  Missing'}")
        
        if redis_client and operations_ok:
            if not data_exists:
                print("\n🚀 READY FOR INITIALIZATION:")
                print("Run: python3 init_redis_cloud.py")
            else:
                print("\n🎉 REDIS IS READY!")
                print("Run: ./start_redis_ai.sh")
        else:
            print("\n🔧 ISSUES NEED TO BE RESOLVED FIRST")

def main():
    """Main verification function"""
    print("🔍 Redis Cloud Status Verification")
    print("=" * 40)
    
    provide_setup_guidance()

if __name__ == "__main__":
    main()
