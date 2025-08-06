#!/usr/bin/env python3
"""
Create comprehensive Design Twitter problem with detailed examples, constraints, and hints
"""

import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
    username=os.getenv('REDIS_USERNAME'),
    ssl=False,
    decode_responses=True
)

def create_design_twitter_problem():
    """Create comprehensive Design Twitter problem"""
    
    problem = {
        'id': 'design_twitter',
        'title': 'Design Twitter',
        'description': '''Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:

• Twitter() Initializes your twitter object.
• void postTweet(int userId, int tweetId) Composes a new tweet with ID tweetId by the user userId. Each call to this function will be made with a unique tweetId.
• List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themselves. Tweets must be ordered from most recent to least recent.
• void follow(int followerId, int followeeId) The user with ID followerId started following the user with ID followeeId.
• void unfollow(int followerId, int followeeId) The user with ID followerId started unfollowing the user with ID followeeId.

Note: A user cannot follow themselves, but they can see their own tweets in their news feed.''',
        'difficulty': 'medium',
        'topic': 'heaps',
        'examples': json.dumps([
            {
                'input': '''Twitter twitter = new Twitter();
twitter.postTweet(1, 5); // User 1 posts a new tweet (id = 5).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
twitter.follow(1, 2);    // User 1 follows user 2.
twitter.postTweet(2, 6); // User 2 posts a new tweet (id = 6).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should come before tweet id 5 because it is posted after tweet id 5.
twitter.unfollow(1, 2);  // User 1 unfollows user 2.
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.''',
                'output': '[null, [5], null, null, [6, 5], null, [5]]',
                'explanation': 'The operations are performed in sequence. User 1 posts tweet 5, gets news feed [5], follows user 2, user 2 posts tweet 6, user 1 gets news feed [6,5] (most recent first), unfollows user 2, and gets news feed [5] (only own tweets).'
            },
            {
                'input': '''Twitter twitter = new Twitter();
twitter.postTweet(1, 1);
twitter.postTweet(2, 2);
twitter.postTweet(1, 3);
twitter.follow(1, 2);
twitter.getNewsFeed(1);''',
                'output': '[null, null, null, null, [3, 2, 1]]',
                'explanation': 'User 1 posts tweets 1 and 3, user 2 posts tweet 2, user 1 follows user 2, then gets news feed showing tweets in chronological order: [3, 2, 1] (most recent first).'
            },
            {
                'input': '''Twitter twitter = new Twitter();
for(int i = 1; i <= 15; i++) {
    twitter.postTweet(1, i);
}
twitter.getNewsFeed(1);''',
                'output': '[15, 14, 13, 12, 11, 10, 9, 8, 7, 6]',
                'explanation': 'User 1 posts 15 tweets (IDs 1-15). The news feed returns only the 10 most recent tweets in reverse chronological order: [15, 14, 13, 12, 11, 10, 9, 8, 7, 6].'
            }
        ]),
        'hints': json.dumps([
            '💡 Use a hash map to store each user\'s followers and a list/queue to store tweets with timestamps. Consider using a max heap to efficiently get the most recent tweets.',
            '💡 For the news feed, you need to merge tweets from the user and all users they follow, then return the 10 most recent. A priority queue (max heap) can help maintain the order efficiently.',
            '💡 Think about the data structures: HashMap for user relationships, HashMap for user tweets, and a global timestamp counter. Use a heap to merge k sorted lists (tweets from followed users) efficiently.'
        ]),
        'constraints': json.dumps([
            '1 ≤ userId, followerId, followeeId ≤ 500',
            '0 ≤ tweetId ≤ 10⁴',
            'All the tweets have unique IDs',
            'At most 3 × 10⁴ calls will be made to postTweet, getNewsFeed, follow, and unfollow'
        ]),
        'tags': json.dumps(['Hash Table', 'Linked List', 'Design', 'Heap (Priority Queue)'])
    }
    
    return problem

def save_problem_to_redis(problem):
    """Save the problem to Redis database"""
    try:
        # Store problem data
        redis_client.hset(f"problem:{problem['id']}", mapping=problem)
        
        # Add to difficulty-topic sorted set
        redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
        
        # Add to topics and difficulties sets
        redis_client.sadd('topics', problem['topic'])
        redis_client.sadd('difficulties', problem['difficulty'])
        
        # Add tags to global tags set and problem-tag mapping
        tags = json.loads(problem['tags'])
        for tag in tags:
            redis_client.sadd('all_tags', tag)
            redis_client.sadd(f'problems_by_tag:{tag.lower().replace(" ", "_").replace("(", "").replace(")", "")}', problem['id'])
        
        print(f"✅ Successfully saved '{problem['title']}' to Redis")
        return True
        
    except Exception as e:
        print(f"❌ Error saving problem to Redis: {e}")
        return False

def create_solution_templates():
    """Create solution templates for different languages"""
    templates = {
        'python': '''class Twitter:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        

    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        Compose a new tweet.
        """
        

    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweet ids in the user's news feed.
        Each item in the news feed must be posted by users who the user followed or by the user themselves.
        Tweets must be ordered from most recent to least recent.
        """
        

    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Follower follows a followee. If the operation is invalid, it should be a no-op.
        """
        

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Follower unfollows a followee. If the operation is invalid, it should be a no-op.
        """
        

# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)''',

        'java': '''class Twitter {
    
    public Twitter() {
        // Initialize your data structure here
        
    }
    
    public void postTweet(int userId, int tweetId) {
        // Compose a new tweet
        
    }
    
    public List<Integer> getNewsFeed(int userId) {
        // Retrieve the 10 most recent tweet ids in the user's news feed
        // Each item must be posted by users who the user followed or by the user themselves
        // Tweets must be ordered from most recent to least recent
        
    }
    
    public void follow(int followerId, int followeeId) {
        // Follower follows a followee
        // If the operation is invalid, it should be a no-op
        
    }
    
    public void unfollow(int followerId, int followeeId) {
        // Follower unfollows a followee
        // If the operation is invalid, it should be a no-op
        
    }
}

/**
 * Your Twitter object will be instantiated and called as such:
 * Twitter obj = new Twitter();
 * obj.postTweet(userId,tweetId);
 * List<Integer> param_2 = obj.getNewsFeed(userId);
 * obj.follow(followerId,followeeId);
 * obj.unfollow(followerId,followeeId);
 */''',

        'cpp': '''class Twitter {
public:
    Twitter() {
        // Initialize your data structure here
        
    }
    
    void postTweet(int userId, int tweetId) {
        // Compose a new tweet
        
    }
    
    vector<int> getNewsFeed(int userId) {
        // Retrieve the 10 most recent tweet ids in the user's news feed
        // Each item must be posted by users who the user followed or by the user themselves
        // Tweets must be ordered from most recent to least recent
        
    }
    
    void follow(int followerId, int followeeId) {
        // Follower follows a followee
        // If the operation is invalid, it should be a no-op
        
    }
    
    void unfollow(int followerId, int followeeId) {
        // Follower unfollows a followee
        // If the operation is invalid, it should be a no-op
        
    }
};

/**
 * Your Twitter object will be instantiated and called as such:
 * Twitter* obj = new Twitter();
 * obj->postTweet(userId,tweetId);
 * vector<int> param_2 = obj->getNewsFeed(userId);
 * obj->follow(followerId,followeeId);
 * obj->unfollow(followerId,followeeId);
 */''',

        'javascript': '''/**
 * Initialize your data structure here.
 */
var Twitter = function() {
    
};

/**
 * Compose a new tweet. 
 * @param {number} userId 
 * @param {number} tweetId
 * @return {void}
 */
Twitter.prototype.postTweet = function(userId, tweetId) {
    
};

/**
 * Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themselves. Tweets must be ordered from most recent to least recent.
 * @param {number} userId
 * @return {number[]}
 */
Twitter.prototype.getNewsFeed = function(userId) {
    
};

/**
 * Follower follows a followee. If the operation is invalid, it should be a no-op.
 * @param {number} followerId 
 * @param {number} followeeId
 * @return {void}
 */
Twitter.prototype.follow = function(followerId, followeeId) {
    
};

/**
 * Follower unfollows a followee. If the operation is invalid, it should be a no-op.
 * @param {number} followerId 
 * @param {number} followeeId
 * @return {void}
 */
Twitter.prototype.unfollow = function(followerId, followeeId) {
    
};

/** 
 * Your Twitter object will be instantiated and called as such:
 * var obj = new Twitter();
 * obj.postTweet(userId,tweetId);
 * var param_2 = obj.getNewsFeed(userId);
 * obj.follow(followerId,followeeId);
 * obj.unfollow(followerId,followeeId);
 */'''
    }
    
    return templates

def main():
    print("🚀 Creating comprehensive Design Twitter problem...")
    
    # Test Redis connection
    try:
        redis_client.ping()
        print("✅ Redis connection successful!")
    except Exception as e:
        print(f"❌ Redis connection failed: {str(e)}")
        return
    
    # Create the problem
    problem = create_design_twitter_problem()
    
    # Save to Redis
    if save_problem_to_redis(problem):
        print(f"📊 Problem Details:")
        print(f"   • Title: {problem['title']}")
        print(f"   • Difficulty: {problem['difficulty']}")
        print(f"   • Topic: {problem['topic']}")
        print(f"   • Tags: {', '.join(json.loads(problem['tags']))}")
        print(f"   • Examples: {len(json.loads(problem['examples']))} detailed examples")
        print(f"   • Hints: {len(json.loads(problem['hints']))} progressive hints")
        print(f"   • Constraints: {len(json.loads(problem['constraints']))} specific constraints")
        
        # Create solution templates
        templates = create_solution_templates()
        print(f"   • Solution templates: {len(templates)} languages")
        
        # Store templates in Redis for quick access
        for lang, template in templates.items():
            redis_client.hset(f"template:{problem['id']}:{lang}", "code", template)
        
        print("\n🎉 Design Twitter problem created successfully!")
        print("Features:")
        print("   ✓ Comprehensive problem description")
        print("   ✓ 3 detailed examples with explanations")
        print("   ✓ 3 progressive hints using heap/priority queue concepts")
        print("   ✓ Realistic constraints")
        print("   ✓ Proper LeetCode-style tags")
        print("   ✓ Multi-language solution templates")
        print("   ✓ Production-ready Redis storage")
        
    else:
        print("❌ Failed to create problem")

if __name__ == "__main__":
    main()
