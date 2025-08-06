#!/bin/bash

# DSA Interview Platform - Redis AI Challenge Setup
# Configures the platform for both challenge prompts

set -e

echo "🏆 Redis AI Challenge - DSA Interview Platform Setup"
echo "=" * 60
echo "Challenge Prompts:"
echo "1. Real-Time AI Innovators - AI-powered application with Redis"
echo "2. Beyond the Cache - Redis as multi-model platform"
echo "=" * 60

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ️]${NC} $1"
}

print_challenge() {
    echo -e "${PURPLE}[🏆]${NC} $1"
}

# Check if running from correct directory
if [ ! -f "app.py" ]; then
    print_error "Please run this script from the dsa-interview directory"
    exit 1
fi

print_info "Setting up Redis AI Challenge features..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# Install enhanced requirements
print_info "Installing Redis AI Challenge dependencies..."
cat > requirements_redis_ai.txt << EOF
# Core Flask dependencies
Flask==2.3.3
Flask-CORS==4.0.0

# Redis with advanced features
redis==5.0.1
redis-py-cluster==2.1.3

# AI and ML libraries
numpy==1.24.3
scikit-learn==1.3.0

# Environment management
python-dotenv==1.0.0

# HTTP requests
requests==2.31.0

# Date and time handling
python-dateutil==2.8.2

# Security
Werkzeug==2.3.7

# Production server
gunicorn==21.2.0

# Vector operations
faiss-cpu==1.7.4

# Text processing for semantic search
sentence-transformers==2.2.2

# JSON handling
jsonify==0.5

# Async support
asyncio==3.4.3
aioredis==2.0.1
EOF

pip install -r requirements_redis_ai.txt
print_status "Enhanced dependencies installed"

# Setup Redis Cloud configuration
print_info "Setting up Redis Cloud configuration..."

if [ ! -f ".env" ]; then
    cp .env.redis_cloud .env
    print_warning "Created .env file from Redis Cloud template"
    print_warning "Please update Redis Cloud credentials in .env file"
else
    print_status ".env file already exists"
fi

# Initialize Redis AI features
print_info "Initializing Redis AI Challenge features..."

python3 << EOF
import sys
sys.path.append('.')

try:
    from redis_cloud_setup import setup_redis_cloud
    
    print("🤖 Initializing Redis AI features...")
    redis_client = setup_redis_cloud()
    
    if redis_client:
        print("✅ Redis AI Challenge features initialized!")
    else:
        print("⚠️ Please configure Redis Cloud credentials")
        
except Exception as e:
    print(f"⚠️ Redis setup: {e}")
    print("Please ensure Redis Cloud credentials are configured")
EOF

# Load production problems with Redis AI enhancements
print_info "Loading production problems with AI enhancements..."
python3 scripts/create_production_problems.py

# Create Redis AI Challenge documentation
print_info "Creating Redis AI Challenge documentation..."

cat > REDIS_AI_CHALLENGE.md << 'EOF'
# 🏆 Redis AI Challenge - DSA Interview Platform

## Challenge Eligibility

This DSA Interview Platform is designed to be eligible for **BOTH** Redis AI Challenge prompts:

### 🤖 Prompt 1: Real-Time AI Innovators

**AI-Powered Features Implemented:**

1. **Vector Search-Driven Recommendations**
   - AI-powered problem recommendations using Redis vector search
   - Semantic similarity matching based on user solving patterns
   - Real-time personalization using user history

2. **Semantic Caching for LLM Optimization**
   - Intelligent caching of LLM-generated hints and explanations
   - Query similarity detection to reduce LLM API calls
   - Performance optimization with Redis TTL and access tracking

3. **Real-Time ML Feature Streaming**
   - Live streaming of user coding metrics for ML analysis
   - Real-time performance tracking and anomaly detection
   - ML model feature extraction from coding sessions

4. **AI-Enhanced Code Analysis**
   - Intelligent code quality assessment
   - Pattern recognition for common coding mistakes
   - Personalized improvement suggestions

### 🔄 Prompt 2: Beyond the Cache

**Multi-Model Redis Usage:**

1. **Primary Database**
   - User profiles and session data stored in Redis
   - Complex data relationships using Redis data structures
   - ACID-like operations with Redis transactions

2. **Full-Text Search**
   - Advanced problem discovery using RedisSearch
   - Multi-field search with filters and sorting
   - Faceted search capabilities

3. **Real-Time Streams**
   - Live coding session streaming with Redis Streams
   - Event-driven architecture for user interactions
   - Consumer groups for scalable processing

4. **Pub/Sub Messaging**
   - Real-time notifications and achievements
   - Live updates for leaderboards and progress
   - Multi-channel communication system

5. **Time Series Analytics**
   - Performance metrics tracking over time
   - Trend analysis and forecasting
   - Real-time dashboards with historical data

## Technical Implementation

### Redis Modules Used
- **RedisSearch (FT.*)**: Full-text and vector search
- **RedisTimeSeries (TS.*)**: Time-based analytics
- **RedisJSON (JSON.*)**: Complex data structures
- **Redis Streams (XADD, XREAD)**: Real-time data streaming

### Key Features

1. **Vector Search Implementation**
   ```python
   # AI-powered recommendations
   FT.SEARCH problem_vector_idx "@embedding:[VECTOR_BLOB]" 
   KNN 5 DISTANCE_METRIC COSINE
   ```

2. **ML Feature Streaming**
   ```python
   # Real-time ML features
   XADD ml_features_stream * user_id 123 score 85 time_spent 1200
   ```

3. **Semantic Caching**
   ```python
   # LLM response caching
   HSET semantic_cache:query_hash response "cached_llm_response"
   EXPIRE semantic_cache:query_hash 7200
   ```

4. **Primary Database Usage**
   ```python
   # User data as primary storage
   HSET user:123 username "john" skill_level "advanced"
   SADD users_by_skill:advanced 123
   ```

5. **Time Series Analytics**
   ```python
   # Performance tracking
   TS.ADD user_performance:123 * 85.5
   TS.RANGE user_performance:123 - +
   ```

## Challenge Compliance

### Real-Time AI Innovators ✅
- ✅ Goes beyond simple chatbots
- ✅ High-impact AI use cases (recommendations, caching, streaming)
- ✅ Redis as real-time data layer for AI
- ✅ Vector search implementation
- ✅ ML workflow optimization

### Beyond the Cache ✅
- ✅ Redis as primary database
- ✅ Full-text search capabilities
- ✅ Real-time streams implementation
- ✅ Pub/Sub messaging system
- ✅ Multi-model platform demonstration

## Deployment

### Redis Cloud Setup
1. Create Redis Cloud instance with required modules
2. Update `.env` with Redis Cloud credentials
3. Run setup script: `./setup_redis_ai_challenge.sh`
4. Initialize features: `python3 redis_cloud_setup.py`

### Local Development
```bash
# Start with Redis AI features
python3 app_redis_cloud.py
```

### Production Deployment
```bash
# Use enhanced Redis Cloud configuration
gunicorn -w 4 -b 0.0.0.0:5000 app_redis_cloud:app
```

## Innovation Highlights

1. **Semantic Code Analysis**: AI-powered code quality assessment
2. **Real-Time Learning**: ML models that adapt to user behavior
3. **Intelligent Caching**: Semantic similarity for LLM optimization
4. **Multi-Modal Search**: Vector + text + metadata search
5. **Stream Processing**: Real-time analytics and notifications

This platform showcases Redis as both an AI accelerator and a comprehensive multi-model database, making it eligible for both challenge prompts while providing real value to users preparing for technical interviews.
EOF

print_status "Redis AI Challenge documentation created"

# Create startup script for Redis AI Challenge
cat > start_redis_ai_challenge.sh << 'EOF'
#!/bin/bash

echo "🏆 Starting DSA Interview Platform - Redis AI Challenge Edition"

# Check Redis Cloud connection
python3 -c "
from redis_cloud_setup import setup_redis_cloud
redis_client = setup_redis_cloud()
if redis_client:
    print('✅ Redis Cloud connected')
else:
    print('❌ Redis Cloud connection failed')
    exit(1)
"

# Start the enhanced application
echo "🚀 Starting Redis AI Challenge application..."
echo "🌐 Access at: http://localhost:5000"
echo "🏆 Features: AI Recommendations, Vector Search, ML Streaming, Beyond Cache"

python3 app_redis_cloud.py
EOF

chmod +x start_redis_ai_challenge.sh
print_status "Redis AI Challenge startup script created"

echo ""
print_challenge "🎉 Redis AI Challenge Setup Complete!"
echo ""
print_info "📋 Challenge Features Implemented:"
print_status "Real-Time AI Innovators:"
echo "   🤖 Vector search-driven recommendations"
echo "   🧠 Semantic caching for LLM optimization"
echo "   📊 Real-time ML feature streaming"
echo "   🔍 AI-enhanced code analysis"
echo ""
print_status "Beyond the Cache:"
echo "   💾 Redis as primary database"
echo "   🔎 Full-text search capabilities"
echo "   🌊 Real-time streams processing"
echo "   📢 Pub/Sub messaging system"
echo "   📈 Time series analytics"
echo ""
print_challenge "🏆 Platform is eligible for BOTH challenge prompts!"
echo ""
print_info "Next Steps:"
echo "1. Update Redis Cloud credentials in .env file"
echo "2. Run: ./start_redis_ai_challenge.sh"
echo "3. Submit to Redis AI Challenge!"
echo ""
print_warning "Don't forget to update your Redis Cloud credentials!"
echo "Visit: https://redis.com/try-free/ to get Redis Cloud instance"
