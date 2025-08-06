# 🚀 DSA Interview Platform

A comprehensive Data Structures & Algorithms interview preparation platform with AI-powered analysis and senior technical recruiter insights.

Project snapshots:-

<img width="1920" height="3199" alt="screencapture-127-0-0-1-5000-2025-08-06-21_16_24" src="https://github.com/user-attachments/assets/a45debcc-8a3f-4c72-88cc-0f1e990a0d4c" />

<img width="1896" height="923" alt="Screenshot 2025-08-06 211743" src="https://github.com/user-attachments/assets/16ac2016-5243-4160-bd69-0acc694985ad" />

<img width="1863" height="1058" alt="Screenshot 2025-08-06 211759" src="https://github.com/user-attachments/assets/5a476ab9-ea68-4ab1-bbd7-70a08c999a82" />
<img width="1897" height="1046" alt="Screenshot 2025-08-06 211806" src="https://github.com/user-attachments/assets/b6fd7bae-87c2-4fce-818b-7b7c520c171c" />

This project is live here:- [DSA Interview Ready](https://dsa-interview-ready.onrender.com)

---

## ✨ Features

### 🎯 Core Functionalities
- **Interactive Problem Solving**: Practice DSA problems with multiple programming languages (4)
- **AI-Powered Code Analysis**: Get detailed feedback on your solutions
- **Senior Recruiter Insights**: Professional evaluation from a senior recruitor perspective
- **Comprehensive Analytics**: Track your progress with detailed metrics
- **Tag-Based Problem Discovery**: Find problems by specific topics and/or level of difficulties

### 📊 Analysis & Insights
- **Technical Skills Assessment**: Problem solving, code quality, algorithm knowledge
- **Communication Skills Evaluation**: Explanation clarity, thought process, confidence
- **Hiring Recommendations**: Professional assessment of interview readiness
- **Topic Performance Tracking**: Detailed breakdown by data structure/algorithm
- **Personalized Action Items**: Targeted improvement recommendations

### 🏷️ Problem Categories
- **Arrays**: Two Sum, Best Time to Buy/Sell Stock, Maximum Subarray
- **Strings**: Valid Anagram, Longest Substring, Valid Palindrome
- **Linked Lists**: Reverse List, Merge Sorted Lists
- **Trees**: Serialize/Deserialize, Maximum Depth
- **Graphs**: Course Schedule, DFS/BFS problems
- **Heaps**: Design Twitter, Merge K Sorted Lists, Top K Elements
- **Dynamic Programming**: Longest Increasing Subsequence
- **And more to come**...

---

## 🛠️ Technology Stack

- **Backend**: Python Flask 2.3.3
- **Database**: Redis Cloud (using redis-py 5.0.1 client)
- **Frontend**: HTML5, CSS3, JS, Tailwind CSS (CDN)
- **AI Features**: 
  - Groq API (for code analysis using llama3-8b-8192 model)
  - AssemblyAI API (for voice transcription)
  - Custom Redis-based AI features for real-time analytics
- **Production Server**: Gunicorn 21.2.0
- **Additional Libraries**:
  - Flask-CORS 4.0.0 (for cross-origin requests)
  - python-dotenv 1.0.0 (environment management)
  - requests 2.31.0 (HTTP client)
  - python-dateutil 2.8.2 (date/time handling)
  - numpy 1.24.3 & scikit-learn 1.3.0 (data processing)


## 🔴 Redis Features Used

- **Core Data Structures**: Hashes for problem/user storage, Sets for categorization, Sorted Sets for progress tracking, Keys/Scan for bulk
operations

- **Vector Search**: AI-powered problem recommendations using vector similarity matching for personalized coding challenges

- **TimeSeries**: Real-time analytics tracking user activity, submission patterns, and search metrics with temporal data points

- **Redis Search**: Full-text search indexing for problem discovery and content filtering across coding challenges

- **Redis JSON**: Complex data logging and structured analytics storage for AI analysis results and user interaction data

- **Multi-Model Database**: Combined hash-based problem storage, set-based categorization, time-series analytics, and vector search for a
complete DSA interview platform


## 📋 Prerequisites

- Python 3.8+
- Redis Server
- Git

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Divya4879/DSA-Interview-Ready.git
cd dsa-interview
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Redis
```bash
# On Ubuntu/Debian
sudo apt-get install redis-server

# On macOS
brew install redis

# Start Redis
redis-server --daemonize yes
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your Redis configuration, Assembly AI API & Grog AI API keys 
```

### 6. Initialize Database
```bash
python3 scripts/create_production_problems.py
python3 scripts/create_tagged_problems.py
```

### 7. Start the Application
```bash
# Option 1: Use the quick start script
./start_server.sh

# Option 2: Manual start
python3 app.py
```


### 8. Access the Platform
Open your browser and navigate to: `http://localhost:5000`

---

## 📁 Project Structure

```
dsa-interview/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment configuration
├── start_server.sh       # Quick start script
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── practice.html
│   └── analysis.html
├── static/              # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── scripts/             # Database initialization scripts
    ├── create_production_problems.py
    └── create_tagged_problems.py
```

---

## 🎮 Usage Guide

### Dashboard
- View your overall progress and statistics
- Quick access to recent problems solved
- Interview readiness assessment

### Practice Mode
- Select difficulty level (Easy, Medium, Hard)
- Choose topic (Arrays, Strings, Trees, etc.)
- Filter by programming language
- Solve problems with real-time feedback
- Comprehensive technical skills assessment
- Communication and soft skills evaluation
- Senior recruiter insights and recommendations
- Personalized action to-dos for improvement

## 🏷️ Problem Tags

Problems are categorized with industry-standard tags:
- **Data Structures**: Array, Hash Table, Linked List, Tree, Graph, Heap
- **Algorithms**: Two Pointers, Binary Search, DFS, BFS, Dynamic Programming
- **Techniques**: Sliding Window, Divide and Conquer, Greedy, Sorting

---

## 📊 Analytics Features

### Technical Metrics
- Problem solving score (1-10)
- Code quality assessment
- Algorithm knowledge evaluation
- Time complexity analysis skills

### Communication Metrics
- Explanation clarity
- Thought process articulation
- Question handling ability
- Confidence level assessment

### Progress Tracking
- Problems solved over time
- Success rate by difficulty
- Topic mastery progression
- Consistency scoring

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_USERNAME=

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Application Configuration
APP_NAME=DSA Interview Platform
APP_VERSION=1.0.0

# AI Service API Keys
GROQ_API_KEY=
ASSEMBLYAI_API_KEY=

# Application URLs
BASE_URL=http://localhost:5000
```

---

## 🚀 Deployment

### Local Development

```bash
# Option 1: Using the provided script (recommended)
./start_server.sh
```

#### Option 2: Manual setup
```
source venv/bin/activate
export FLASK_ENV=development
export FLASK_DEBUG=True
python3 app.py
```


### Production Deployment (Render)

Environment Variables Required:
```bash
# Set these in Render dashboard
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key
REDIS_HOST=your-redis-cloud-host
REDIS_PORT=your-redis-cloud-port
REDIS_PASSWORD=your-redis-cloud-password
REDIS_USERNAME=default
GROQ_API_KEY=your-groq-api-key
ASSEMBLYAI_API_KEY=your-assemblyai-api-key
```

Render Configuration:
```yaml
# render.yaml (already configured)
buildCommand: "pip install -r requirements.txt"
startCommand: "gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
```

Manual Production Deployment:
```bash
# For other platforms (not Render)
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:5000 --workers 4 --timeout 120 --max-requests 1000
```
---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---


## 🚀 Future Plans for this Project

-  Additional programming languages support
-  More advanced AI analysis features
-  Integration with external coding platforms
-  Mobile responsive improvements
-  Real-time collaborative solving

---

**Built with ❤️ for aspiring techies wanting to crack relevant jobs, or just for DSA mastery**

*Master your DSA skills with AI-powered insights and professional feedback!*
