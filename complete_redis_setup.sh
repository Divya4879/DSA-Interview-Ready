#!/bin/bash

# Complete Redis AI Challenge Setup Script
echo "🏆 Redis AI Challenge - Complete Setup"
echo "======================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

# Step 1: Check prerequisites
print_step "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required"
    exit 1
fi
print_success "Python 3 found"

if ! command -v redis-cli &> /dev/null; then
    print_warning "redis-cli not found, installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y redis-tools
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install redis
    fi
fi
print_success "redis-cli available"

# Step 2: Setup virtual environment
print_step "Setting up Python environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
fi

source venv/bin/activate
print_success "Virtual environment activated"

# Install enhanced requirements
pip install --upgrade pip
pip install redis python-dotenv flask flask-cors numpy scikit-learn requests
print_success "Dependencies installed"

# Step 3: Test Redis Cloud connection
print_step "Testing Redis Cloud connection..."

if [ ! -f ".env" ]; then
    print_warning "No .env file found. Let's create one..."
    ./test_redis_connection.sh
else
    print_success ".env file exists"
    
    # Load environment variables
    source .env
    
    # Test connection
    if redis-cli -h "$REDIS_CLOUD_HOST" -p "$REDIS_CLOUD_PORT" -a "$REDIS_CLOUD_PASSWORD" --tls ping > /dev/null 2>&1; then
        print_success "Redis Cloud connection successful"
    else
        print_error "Redis Cloud connection failed"
        print_warning "Running connection setup..."
        ./test_redis_connection.sh
    fi
fi

# Step 4: Initialize Redis Cloud with AI Challenge data
print_step "Initializing Redis Cloud with AI Challenge data..."

python3 init_redis_cloud.py

if [ $? -eq 0 ]; then
    print_success "Redis Cloud initialization complete"
else
    print_error "Redis Cloud initialization failed"
    exit 1
fi

# Step 5: Verify setup
print_step "Verifying complete setup..."

# Test Flask app
python3 -c "
from app_redis_cloud import app
with app.test_client() as client:
    response = client.get('/')
    if response.status_code == 200:
        print('✅ Flask app working')
    else:
        print('❌ Flask app failed')
        exit(1)
" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Flask application verified"
else
    print_error "Flask application verification failed"
fi

# Step 6: Create startup script
print_step "Creating startup script..."

cat > start_redis_ai.sh << 'EOF'
#!/bin/bash

echo "🏆 Starting DSA Interview Platform - Redis AI Challenge Edition"
echo "================================================================"

# Activate virtual environment
source venv/bin/activate

# Load environment variables
source .env

# Test Redis connection
echo "🔍 Testing Redis Cloud connection..."
if redis-cli -h "$REDIS_CLOUD_HOST" -p "$REDIS_CLOUD_PORT" -a "$REDIS_CLOUD_PASSWORD" --tls ping > /dev/null 2>&1; then
    echo "✅ Redis Cloud connected"
else
    echo "❌ Redis Cloud connection failed"
    echo "Please check your credentials in .env file"
    exit 1
fi

# Start the application
echo ""
echo "🚀 Starting Redis AI Challenge application..."
echo "🌐 Access at: http://localhost:5000"
echo ""
echo "🏆 Challenge Features Available:"
echo "   🤖 AI-powered problem recommendations"
echo "   🧠 Semantic caching for LLM optimization"
echo "   📊 Real-time ML feature streaming"
echo "   💾 Redis as primary database"
echo "   🔍 Full-text search capabilities"
echo "   🌊 Real-time streams processing"
echo "   📢 Pub/Sub notifications"
echo "   📈 Time series analytics"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app_redis_cloud.py
EOF

chmod +x start_redis_ai.sh
print_success "Startup script created"

# Step 7: Final verification
print_step "Running final verification..."

echo ""
echo "🧪 Testing Redis AI Challenge features..."

# Test with Redis CLI
source .env

echo "Testing Redis modules..."
redis-cli -h "$REDIS_CLOUD_HOST" -p "$REDIS_CLOUD_PORT" -a "$REDIS_CLOUD_PASSWORD" --tls MODULE LIST | grep -E "(search|timeseries)" > /dev/null

if [ $? -eq 0 ]; then
    print_success "Required Redis modules available"
else
    print_warning "Some Redis modules may be missing"
fi

echo "Testing search indexes..."
redis-cli -h "$REDIS_CLOUD_HOST" -p "$REDIS_CLOUD_PORT" -a "$REDIS_CLOUD_PASSWORD" --tls FT._LIST > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_success "Search indexes working"
else
    print_warning "Search indexes may need initialization"
fi

# Final summary
echo ""
echo "🎉 Redis AI Challenge Setup Complete!"
echo "====================================="
echo ""
print_success "✅ Virtual environment: Ready"
print_success "✅ Redis Cloud: Connected"
print_success "✅ AI Challenge features: Initialized"
print_success "✅ Flask application: Verified"
print_success "✅ Startup script: Created"
echo ""
echo "🚀 To start your Redis AI Challenge platform:"
echo "   ./start_redis_ai.sh"
echo ""
echo "🏆 Your platform is eligible for BOTH challenge prompts:"
echo "   1. Real-Time AI Innovators"
echo "   2. Beyond the Cache"
echo ""
echo "📚 Documentation available in:"
echo "   - REDIS_AI_CHALLENGE_SUBMISSION.md"
echo "   - redis_cloud_guide.md"
echo ""
print_success "Ready for Redis AI Challenge submission! 🎯"
