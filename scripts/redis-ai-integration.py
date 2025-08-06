import redis
import json
from datetime import datetime
import asyncio
import os
from groq import Groq
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

class RedisAIIntegration:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
    def generate_embeddings(self, text):
        """Generate vector embeddings using Groq API for semantic search"""
        try:
            # Use Groq to generate a semantic representation
            prompt = f"""
            Convert this text into a semantic vector representation as a list of 10 numbers between -1 and 1:
            Text: {text}
            
            Return only a JSON array of 10 float numbers, nothing else.
            """
            
            response = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.1,
                max_tokens=100
            )
            
            # Parse the response to get embeddings
            import json
            try:
                embeddings = json.loads(response.choices[0].message.content)
                return embeddings if len(embeddings) == 10 else [0.0] * 10
            except:
                # Fallback to simple hash-based representation
                return [hash(text[i:i+5]) % 100 / 100.0 for i in range(0, min(50, len(text)), 5)][:10]
                
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            # Simple fallback
            return [0.1] * 10
    
    def store_journal_with_vectors(self, journal_entry):
        """Store journal entry with vector embeddings for semantic search"""
        
        # Generate embedding for the content
        embedding = self.generate_embeddings(journal_entry['content'])
        
        # Store in Redis with vector
        journal_data = {
            **journal_entry,
            'embedding': json.dumps(embedding),
            'created_at': datetime.now().isoformat()
        }
        
        # Store in hash
        self.redis_client.hset(f"journal:{journal_entry['id']}", mapping=journal_data)
        
        # Add to sorted set for time-based queries
        self.redis_client.zadd(
            f"user:{journal_entry['user_id']}:journals",
            {journal_entry['id']: datetime.now().timestamp()}
        )
        
        # Update real-time stream
        self.redis_client.xadd('journal_stream', {
            'user_id': journal_entry['user_id'],
            'type': 'new_entry',
            'entry_id': journal_entry['id'],
            'mood_score': journal_entry.get('mood_score', 0)
        })
        
        print(f"✓ Stored journal entry {journal_entry['id']} with vector embeddings")
    
    def semantic_search_journals(self, user_id, query, limit=5):
        """Perform semantic search using Groq API"""
        
        # Get all journal IDs for user
        journal_ids = self.redis_client.zrange(f"user:{user_id}:journals", 0, -1)
        
        if not journal_ids:
            return []
        
        try:
            # Use Groq to find semantically similar entries
            journal_contents = []
            for journal_id in journal_ids:
                journal_data = self.redis_client.hgetall(f"journal:{journal_id}")
                if journal_data and 'content' in journal_data:
                    journal_contents.append({
                        'id': journal_id,
                        'content': journal_data['content'],
                        'timestamp': journal_data.get('created_at', '')
                    })
        
        if not journal_contents:
            return []
        
        # Create prompt for Groq to find similar entries
        entries_text = "\n".join([f"ID: {entry['id']}, Content: {entry['content']}" for entry in journal_contents])
        
        prompt = f"""
        Find the most semantically similar journal entries to this query: "{query}"
        
        Available entries:
        {entries_text}
        
        Return the top {limit} most similar entry IDs as a JSON array, ordered by relevance.
        Consider emotional content, topics, and context when determining similarity.
        """
        
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.2,
            max_tokens=200
        )
        
        import json
        try:
            similar_ids = json.loads(response.choices[0].message.content)
            results = []
            
            for journal_id in similar_ids:
                journal_data = self.redis_client.hgetall(f"journal:{journal_id}")
                if journal_data:
                    results.append({
                        'journal_id': journal_id,
                        'similarity': 0.9,  # Placeholder since Groq determined relevance
                        'content': journal_data['content'],
                        'timestamp': journal_data.get('created_at', '')
                    })
            
            return results[:limit]
            
        except:
            # Fallback to simple text matching
            return self._simple_text_search(journal_contents, query, limit)
            
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return self._simple_text_search(journal_contents, query, limit)

    def _simple_text_search(self, journal_contents, query, limit):
        """Simple fallback text search"""
        query_words = query.lower().split()
        results = []
        
        for entry in journal_contents:
            content_lower = entry['content'].lower()
            score = sum(1 for word in query_words if word in content_lower)
            
            if score > 0:
                results.append({
                    'journal_id': entry['id'],
                    'similarity': score / len(query_words),
                    'content': entry['content'],
                    'timestamp': entry['timestamp']
                })
        
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]
    
    def update_user_analytics(self, user_id):
        """Update real-time analytics using Redis streams and sorted sets"""
        
        # Get recent activities from stream
        activities = self.redis_client.xrange('activity_stream', count=100)
        
        daily_stats = {'journal': 0, 'workout': 0, 'study': 0}
        mood_scores = []
        
        for activity in activities:
            activity_data = activity[1]
            if activity_data.get('user_id') == user_id:
                activity_type = activity_data.get('type')
                if activity_type in daily_stats:
                    daily_stats[activity_type] += 1
                
                # Extract mood data
                data = json.loads(activity_data.get('data', '{}'))
                if 'mood_score' in data:
                    mood_scores.append(data['mood_score'])
        
        # Update analytics in Redis
        analytics_key = f"user:{user_id}:analytics:daily"
        self.redis_client.hset(analytics_key, mapping={
            **daily_stats,
            'avg_mood': 0,
            'last_updated': datetime.now().isoformat()
        })
        
        # Set expiration for daily analytics
        self.redis_client.expire(analytics_key, 86400)  # 24 hours
        
        print(f"✓ Updated analytics for user {user_id}")
    
    def get_adaptive_learning_data(self, user_id, subject=None):
        """Get adaptive learning recommendations using Redis data"""
        
        # Get academic performance data
        academic_data = self.redis_client.hgetall(f"academic:{user_id}")
        
        if not academic_data:
            return {"message": "No academic data found"}
        
        # Analyze weak areas using Redis sorted sets
        weak_areas = []
        strong_areas = []
        
        # This would typically involve more complex analysis
        # For demo, we'll use simple threshold-based logic
        
        performance_key = f"user:{user_id}:performance"
        all_scores = self.redis_client.zrange(performance_key, 0, -1, withscores=True)
        
        for topic, score in all_scores:
            if score < 75:  # Threshold for weak areas
                weak_areas.append({'topic': topic, 'score': score})
            elif score > 85:  # Threshold for strong areas
                strong_areas.append({'topic': topic, 'score': score})
        
        return {
            'weak_areas': weak_areas,
            'strong_areas': strong_areas,
            'recommendations': self._generate_study_recommendations(weak_areas)
        }
    
    def _generate_study_recommendations(self, weak_areas):
        """Generate study recommendations based on weak areas"""
        recommendations = []
        
        for area in weak_areas:
            recommendations.append({
                'topic': area['topic'],
                'suggestion': f"Focus on {area['topic']} - current score: {area['score']}%",
                'priority': 'high' if area['score'] < 60 else 'medium'
            })
        
        return recommendations
    
    def cache_ai_response(self, cache_key, response, ttl=3600):
        """Cache AI model responses to improve performance"""
        self.redis_client.setex(cache_key, ttl, json.dumps(response))
    
    def get_cached_ai_response(self, cache_key):
        """Retrieve cached AI response"""
        cached = self.redis_client.get(cache_key)
        return json.loads(cached) if cached else None

# Example usage
if __name__ == "__main__":
    ai_integration = RedisAIIntegration()
    
    # Example journal entry
    sample_journal = {
        'id': 'journal_test_1',
        'user_id': 'user_123',
        'content': 'Today I learned about machine learning and felt excited about the possibilities.',
        'mood_score': 8,
        'emotions': ['excited', 'curious', 'motivated']
    }
    
    # Store with vector embeddings
    ai_integration.store_journal_with_vectors(sample_journal)
    
    # Perform semantic search
    results = ai_integration.semantic_search_journals('user_123', 'learning and education')
    print("Semantic search results:", results)
    
    # Update analytics
    ai_integration.update_user_analytics('user_123')
    
    print("Redis AI integration demo complete!")
