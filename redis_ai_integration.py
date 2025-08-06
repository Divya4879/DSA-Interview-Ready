"""
Redis AI Integration for DSA Interview Platform
Adds vector search, time series analytics, and AI-powered features
"""

import redis
import json
import numpy as np
from datetime import datetime
import hashlib
from typing import List, Dict, Any

class RedisAIManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.setup_ai_features()
    
    def setup_ai_features(self):
        """Initialize Redis AI features"""
        try:
            # Setup vector search index for problems
            self.setup_vector_index()
            
            # Setup time series for analytics
            self.setup_time_series()
            
            # Setup JSON documents for complex data
            self.setup_json_features()
            
            print("✅ Redis AI features initialized")
        except Exception as e:
            print(f"⚠️ Redis AI setup warning: {e}")
    
    def setup_vector_index(self):
        """Create vector search index for problem similarity"""
        try:
            # Check if index exists
            self.redis.execute_command("FT.INFO", "problem_similarity")
        except:
            # Create vector index
            try:
                self.redis.execute_command(
                    "FT.CREATE", "problem_similarity",
                    "ON", "HASH",
                    "PREFIX", "1", "problem_vector:",
                    "SCHEMA",
                    "problem_id", "TEXT", "SORTABLE",
                    "title", "TEXT",
                    "description", "TEXT",
                    "topic", "TAG", "SORTABLE",
                    "difficulty", "TAG", "SORTABLE",
                    "companies", "TAG",
                    "embedding", "VECTOR", "FLAT", "6", 
                    "TYPE", "FLOAT32", "DIM", "384", "DISTANCE_METRIC", "COSINE"
                )
                print("✅ Vector search index created")
            except Exception as e:
                print(f"⚠️ Vector index creation failed: {e}")
    
    def setup_time_series(self):
        """Setup time series for real-time analytics"""
        time_series = [
            "user_submissions",
            "problem_views", 
            "ai_analysis_requests",
            "voice_explanations",
            "user_activity",
            "difficulty_trends"
        ]
        
        for ts_name in time_series:
            try:
                self.redis.execute_command(
                    "TS.CREATE", ts_name,
                    "RETENTION", "604800000",  # 7 days
                    "LABELS", "type", "analytics"
                )
            except:
                pass  # Already exists
    
    def setup_json_features(self):
        """Setup JSON document features"""
        try:
            # Test JSON functionality
            self.redis.execute_command("JSON.SET", "test_json", ".", '{"test": true}')
            self.redis.execute_command("JSON.DEL", "test_json")
            print("✅ JSON features available")
        except Exception as e:
            print(f"⚠️ JSON features not available: {e}")
    
    def generate_problem_embedding(self, problem_data: Dict) -> List[float]:
        """Generate embedding for problem (simplified version)"""
        # In production, use actual embedding model (OpenAI, Sentence Transformers, etc.)
        text = f"{problem_data.get('title', '')} {problem_data.get('description', '')}"
        
        # Simple hash-based embedding (replace with real embeddings)
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert to 384-dim vector (simplified)
        embedding = []
        for i in range(0, len(hash_hex), 2):
            val = int(hash_hex[i:i+2], 16) / 255.0
            embedding.append(val)
        
        # Pad to 384 dimensions
        while len(embedding) < 384:
            embedding.append(0.0)
        
        return embedding[:384]
    
    def index_problem_for_similarity(self, problem_id: str, problem_data: Dict):
        """Index a problem for vector similarity search"""
        try:
            embedding = self.generate_problem_embedding(problem_data)
            
            # Convert embedding to bytes
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            
            # Store in Redis with vector
            vector_key = f"problem_vector:{problem_id}"
            self.redis.hset(vector_key, mapping={
                "problem_id": problem_id,
                "title": problem_data.get('title', ''),
                "description": problem_data.get('description', '')[:200],  # Truncate
                "topic": problem_data.get('topic', ''),
                "difficulty": problem_data.get('difficulty', ''),
                "companies": ','.join(problem_data.get('companies', [])),
                "embedding": embedding_bytes
            })
            
        except Exception as e:
            print(f"⚠️ Problem indexing failed for {problem_id}: {e}")
    
    def find_similar_problems(self, problem_id: str, limit: int = 5) -> List[Dict]:
        """Find similar problems using vector search"""
        try:
            # Get the problem's embedding
            vector_key = f"problem_vector:{problem_id}"
            embedding_bytes = self.redis.hget(vector_key, "embedding")
            
            if not embedding_bytes:
                return []
            
            # Search for similar problems
            results = self.redis.execute_command(
                "FT.SEARCH", "problem_similarity",
                f"*=>[KNN {limit + 1} @embedding $embedding]",
                "PARAMS", "2", "embedding", embedding_bytes,
                "RETURN", "3", "problem_id", "title", "difficulty",
                "DIALECT", "2"
            )
            
            # Parse results
            similar_problems = []
            if len(results) > 1:
                for i in range(2, len(results), 2):  # Skip count and original
                    doc = results[i + 1]
                    if len(doc) >= 6:
                        similar_problems.append({
                            "problem_id": doc[1],
                            "title": doc[3],
                            "difficulty": doc[5]
                        })
            
            # Remove the original problem
            similar_problems = [p for p in similar_problems if p["problem_id"] != problem_id]
            
            return similar_problems[:limit]
            
        except Exception as e:
            print(f"⚠️ Similarity search failed: {e}")
            return []
    
    def track_user_activity(self, user_id: str, activity_type: str, metadata: Dict = None):
        """Track user activity in time series"""
        try:
            timestamp = int(datetime.now().timestamp() * 1000)
            
            # Add to time series
            self.redis.execute_command(
                "TS.ADD", "user_activity", timestamp, 1,
                "LABELS", "user_id", user_id, "activity", activity_type
            )
            
            # Store detailed activity in JSON
            activity_key = f"activity:{user_id}:{timestamp}"
            activity_data = {
                "user_id": user_id,
                "activity_type": activity_type,
                "timestamp": timestamp,
                "metadata": metadata or {}
            }
            
            self.redis.execute_command(
                "JSON.SET", activity_key, ".", json.dumps(activity_data)
            )
            
            # Set expiration (7 days)
            self.redis.expire(activity_key, 604800)
            
        except Exception as e:
            print(f"⚠️ Activity tracking failed: {e}")
    
    def get_real_time_analytics(self) -> Dict:
        """Get real-time analytics from time series"""
        try:
            now = int(datetime.now().timestamp() * 1000)
            hour_ago = now - (60 * 60 * 1000)
            
            analytics = {}
            
            # Get submissions in last hour
            try:
                submissions = self.redis.execute_command(
                    "TS.RANGE", "user_submissions", hour_ago, now,
                    "AGGREGATION", "count", 300000  # 5-minute buckets
                )
                analytics["submissions_last_hour"] = len(submissions)
            except:
                analytics["submissions_last_hour"] = 0
            
            # Get problem views
            try:
                views = self.redis.execute_command(
                    "TS.RANGE", "problem_views", hour_ago, now,
                    "AGGREGATION", "count", 300000
                )
                analytics["views_last_hour"] = len(views)
            except:
                analytics["views_last_hour"] = 0
            
            # Get AI analysis requests
            try:
                ai_requests = self.redis.execute_command(
                    "TS.RANGE", "ai_analysis_requests", hour_ago, now,
                    "AGGREGATION", "count", 300000
                )
                analytics["ai_requests_last_hour"] = len(ai_requests)
            except:
                analytics["ai_requests_last_hour"] = 0
            
            return analytics
            
        except Exception as e:
            print(f"⚠️ Analytics retrieval failed: {e}")
            return {}
    
    def cache_ai_analysis(self, problem_id: str, code: str, analysis: Dict):
        """Cache AI analysis results with semantic similarity"""
        try:
            # Create cache key based on problem and code hash
            code_hash = hashlib.md5(f"{problem_id}:{code}".encode()).hexdigest()
            cache_key = f"ai_analysis:{code_hash}"
            
            # Store as JSON with TTL
            self.redis.execute_command(
                "JSON.SET", cache_key, ".", json.dumps({
                    "problem_id": problem_id,
                    "code_hash": code_hash,
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat(),
                    "cached": True
                })
            )
            
            # Set expiration (1 hour)
            self.redis.expire(cache_key, 3600)
            
            # Track AI request
            self.redis.execute_command(
                "TS.ADD", "ai_analysis_requests", 
                int(datetime.now().timestamp() * 1000), 1
            )
            
        except Exception as e:
            print(f"⚠️ AI analysis caching failed: {e}")
    
    def get_cached_ai_analysis(self, problem_id: str, code: str) -> Dict:
        """Get cached AI analysis if available"""
        try:
            code_hash = hashlib.md5(f"{problem_id}:{code}".encode()).hexdigest()
            cache_key = f"ai_analysis:{code_hash}"
            
            cached_data = self.redis.execute_command("JSON.GET", cache_key)
            if cached_data:
                return json.loads(cached_data)
            
        except Exception as e:
            print(f"⚠️ AI analysis cache retrieval failed: {e}")
        
        return None
    
    def get_user_recommendations(self, user_id: str) -> List[Dict]:
        """Get personalized problem recommendations"""
        try:
            # Get user's recent submissions
            user_problems = self.redis.zrevrange(f"user:{user_id}:submissions", 0, 4)
            
            if not user_problems:
                # Return popular problems for new users
                return self.get_trending_problems()
            
            # Find similar problems to user's recent submissions
            recommendations = []
            for problem_id in user_problems:
                similar = self.find_similar_problems(problem_id, 2)
                recommendations.extend(similar)
            
            # Remove duplicates and limit
            seen = set()
            unique_recommendations = []
            for rec in recommendations:
                if rec["problem_id"] not in seen:
                    seen.add(rec["problem_id"])
                    unique_recommendations.append(rec)
            
            return unique_recommendations[:5]
            
        except Exception as e:
            print(f"⚠️ Recommendations failed: {e}")
            return []
    
    def get_trending_problems(self) -> List[Dict]:
        """Get trending problems based on recent activity"""
        try:
            # Get most viewed problems in last 24 hours
            trending_key = "trending_problems"
            trending = self.redis.zrevrange(trending_key, 0, 4, withscores=True)
            
            problems = []
            for problem_id, score in trending:
                problem_data = self.redis.hgetall(f"problem:{problem_id}")
                if problem_data:
                    problems.append({
                        "problem_id": problem_id,
                        "title": problem_data.get("title", ""),
                        "difficulty": problem_data.get("difficulty", ""),
                        "views": int(score)
                    })
            
            return problems
            
        except Exception as e:
            print(f"⚠️ Trending problems failed: {e}")
            return []

# Integration functions for your main app
def init_redis_ai(redis_client):
    """Initialize Redis AI manager"""
    return RedisAIManager(redis_client)

def enhance_problem_with_ai(redis_ai, problem_id, problem_data):
    """Enhance problem with AI features"""
    # Index for similarity search
    redis_ai.index_problem_for_similarity(problem_id, problem_data)
    
    # Track problem view
    redis_ai.redis.zincrby("trending_problems", 1, problem_id)
    
    return problem_data
