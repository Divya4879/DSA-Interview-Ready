import redis
import json
from datetime import datetime, timedelta
import numpy as np

# Redis connection setup
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def setup_redis_schema():
    """Set up Redis data structures for the LifeSync AI application"""
    
    print("Setting up Redis schema for LifeSync AI...")
    
    # Create indexes for vector search
    try:
        # Journal entries with vector embeddings for semantic search
        r.ft('journal_idx').create_index([
            'user_id', 'timestamp', 'content', 'mood_score', 
            'emotions', 'gratitude_level', 'embedding'
        ])
        print("✓ Created journal index")
    except:
        print("Journal index already exists")
    
    try:
        # Workout entries for fitness tracking
        r.ft('workout_idx').create_index([
            'user_id', 'date', 'type', 'duration', 'pre_mood', 
            'post_mood', 'exercises', 'mood_improvement'
        ])
        print("✓ Created workout index")
    except:
        print("Workout index already exists")
    
    try:
        # Academic data for adaptive learning
        r.ft('academic_idx').create_index([
            'user_id', 'subject', 'topic', 'subtopic', 'test_scores',
            'performance_vector', 'weak_areas'
        ])
        print("✓ Created academic index")
    except:
        print("Academic index already exists")
    
    # Set up Redis streams for real-time data processing
    try:
        # Activity stream for real-time updates
        r.xgroup_create('activity_stream', 'processors', id='0', mkstream=True)
        print("✓ Created activity stream")
    except:
        print("Activity stream already exists")
    
    # Initialize user analytics keys
    analytics_keys = [
        'user:analytics:daily',
        'user:analytics:weekly', 
        'user:analytics:monthly',
        'user:productivity:hourly',
        'user:mood:trends'
    ]
    
    for key in analytics_keys:
        if not r.exists(key):
            r.hset(key, mapping={'initialized': str(datetime.now())})
    
    print("✓ Initialized analytics keys")
    
    # Set up caching for AI model responses
    r.config_set('maxmemory-policy', 'allkeys-lru')
    print("✓ Configured LRU cache policy")
    
    print("\nRedis setup complete! Ready for LifeSync AI application.")

def seed_sample_data():
    """Seed some sample data for demonstration"""
    
    print("\nSeeding sample data...")
    
    # Sample journal entries
    sample_journals = [
        {
            'id': 'journal_1',
            'user_id': 'user_123',
            'content': 'Had a great day today! Completed all my tasks and felt very productive.',
            'timestamp': datetime.now().isoformat(),
            'mood_score': 8,
            'emotions': ['happy', 'productive', 'satisfied'],
            'gratitude_level': 7
        },
        {
            'id': 'journal_2', 
            'user_id': 'user_123',
            'content': 'Feeling a bit overwhelmed with work, but managed to get through it.',
            'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
            'mood_score': 5,
            'emotions': ['stressed', 'overwhelmed', 'resilient'],
            'gratitude_level': 4
        }
    ]
    
    for journal in sample_journals:
        r.hset(f"journal:{journal['id']}", mapping=journal)
        # Add to activity stream
        r.xadd('activity_stream', {
            'type': 'journal',
            'user_id': journal['user_id'],
            'data': json.dumps(journal)
        })
    
    print("✓ Seeded journal entries")
    
    # Sample workout data
    sample_workouts = [
        {
            'id': 'workout_1',
            'user_id': 'user_123',
            'date': datetime.now().date().isoformat(),
            'type': 'Cardio',
            'duration': 45,
            'pre_mood': 6,
            'post_mood': 8,
            'exercises': ['Running', 'Cycling'],
            'mood_improvement': 2
        }
    ]
    
    for workout in sample_workouts:
        r.hset(f"workout:{workout['id']}", mapping=workout)
        r.xadd('activity_stream', {
            'type': 'workout',
            'user_id': workout['user_id'], 
            'data': json.dumps(workout)
        })
    
    print("✓ Seeded workout entries")
    
    # Sample academic data
    sample_academic = {
        'user_123': {
            'subjects': ['Mathematics', 'Physics', 'Chemistry'],
            'performance': {
                'Mathematics': {'calculus': 85, 'algebra': 92, 'geometry': 78},
                'Physics': {'mechanics': 88, 'thermodynamics': 75, 'optics': 82},
                'Chemistry': {'organic': 90, 'inorganic': 85, 'physical': 80}
            }
        }
    }
    
    r.hset('academic:user_123', mapping=sample_academic['user_123'])
    print("✓ Seeded academic data")
    
    print("Sample data seeding complete!")

if __name__ == "__main__":
    setup_redis_schema()
    seed_sample_data()
