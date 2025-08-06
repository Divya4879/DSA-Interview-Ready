#!/usr/bin/env python3
"""
Create production-ready problems with comprehensive details
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

def create_problem(id, title, description, difficulty, topic, examples, hints, constraints, tags):
    return {
        'id': id,
        'title': title,
        'description': description,
        'difficulty': difficulty,
        'topic': topic,
        'examples': json.dumps(examples),
        'hints': json.dumps(hints),
        'constraints': json.dumps(constraints),
        'tags': json.dumps(tags)
    }

# Production-ready problems with comprehensive details
production_problems = [
    # HEAPS PROBLEMS
    create_problem(
        'design_twitter', 'Design Twitter',
        '''Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:

• Twitter() Initializes your twitter object.
• void postTweet(int userId, int tweetId) Composes a new tweet with ID tweetId by the user userId. Each call to this function will be made with a unique tweetId.
• List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet IDs in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user themselves. Tweets must be ordered from most recent to least recent.
• void follow(int followerId, int followeeId) The user with ID followerId started following the user with ID followeeId.
• void unfollow(int followerId, int followeeId) The user with ID followerId started unfollowing the user with ID followeeId.

Note: A user cannot follow themselves, but they can see their own tweets in their news feed.''',
        'medium', 'heaps',
        [
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
        ],
        [
            '💡 Use a hash map to store each user\'s followers and a list/queue to store tweets with timestamps. Consider using a max heap to efficiently get the most recent tweets.',
            '💡 For the news feed, you need to merge tweets from the user and all users they follow, then return the 10 most recent. A priority queue (max heap) can help maintain the order efficiently.',
            '💡 Think about the data structures: HashMap for user relationships, HashMap for user tweets, and a global timestamp counter. Use a heap to merge k sorted lists (tweets from followed users) efficiently.'
        ],
        [
            '1 ≤ userId, followerId, followeeId ≤ 500',
            '0 ≤ tweetId ≤ 10⁴',
            'All the tweets have unique IDs',
            'At most 3 × 10⁴ calls will be made to postTweet, getNewsFeed, follow, and unfollow'
        ],
        ['Hash Table', 'Linked List', 'Design', 'Heap (Priority Queue)']
    ),
    
    create_problem(
        'merge_k_sorted_lists', 'Merge k Sorted Lists',
        '''You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

This is a classic problem that demonstrates the power of heaps for merging multiple sorted sequences efficiently.''',
        'hard', 'heaps',
        [
            {
                'input': 'lists = [[1,4,5],[1,3,4],[2,6]]',
                'output': '[1,1,2,3,4,4,5,6]',
                'explanation': 'The linked-lists are: [1->4->5, 1->3->4, 2->6]. Merging them into one sorted list: 1->1->2->3->4->4->5->6.'
            },
            {
                'input': 'lists = []',
                'output': '[]',
                'explanation': 'No linked lists to merge, return empty list.'
            },
            {
                'input': 'lists = [[]]',
                'output': '[]',
                'explanation': 'Single empty linked list, return empty list.'
            }
        ],
        [
            '💡 Use a min heap to keep track of the smallest current element from each list. This allows you to always pick the globally smallest element next.',
            '💡 Initialize the heap with the first node from each non-empty list. After extracting the minimum, add the next node from the same list to the heap.',
            '💡 The time complexity is O(N log k) where N is the total number of nodes and k is the number of lists. The heap operations take O(log k) time.'
        ],
        [
            'k == lists.length',
            '0 ≤ k ≤ 10⁴',
            '0 ≤ lists[i].length ≤ 500',
            '-10⁴ ≤ lists[i][j] ≤ 10⁴',
            'lists[i] is sorted in ascending order',
            'The sum of lists[i].length will not exceed 10⁴'
        ],
        ['Linked List', 'Divide and Conquer', 'Heap (Priority Queue)', 'Merge Sort']
    ),
    
    create_problem(
        'top_k_frequent_elements', 'Top K Frequent Elements',
        '''Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.''',
        'medium', 'heaps',
        [
            {
                'input': 'nums = [1,1,1,2,2,3], k = 2',
                'output': '[1,2]',
                'explanation': 'Element 1 appears 3 times, element 2 appears 2 times, element 3 appears 1 time. The 2 most frequent elements are [1,2].'
            },
            {
                'input': 'nums = [1], k = 1',
                'output': '[1]',
                'explanation': 'Only one element exists, so it is the most frequent.'
            },
            {
                'input': 'nums = [1,2,3,4,5], k = 3',
                'output': '[1,2,3]',
                'explanation': 'All elements appear once, so any 3 elements can be returned. One possible answer is [1,2,3].'
            }
        ],
        [
            '💡 First count the frequency of each element using a hash map. Then use a min heap of size k to keep track of the k most frequent elements.',
            '💡 Alternative approach: Use a max heap to store all elements by frequency, then extract the top k elements. This is simpler but less space-efficient.',
            '💡 For the follow-up constraint, consider using bucket sort or quickselect algorithm to achieve O(n) average time complexity.'
        ],
        [
            '1 ≤ nums.length ≤ 10⁵',
            'k is in the range [1, the number of unique elements in the array]',
            'It is guaranteed that the answer is unique'
        ],
        ['Array', 'Hash Table', 'Divide and Conquer', 'Sorting', 'Heap (Priority Queue)', 'Bucket Sort', 'Counting', 'Quickselect']
    ),
    
    # DYNAMIC PROGRAMMING PROBLEMS
    create_problem(
        'longest_increasing_subsequence', 'Longest Increasing Subsequence',
        '''Given an integer array nums, return the length of the longest strictly increasing subsequence.

A subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of the remaining elements. For example, [3,6,2,7] is a subsequence of the array [0,3,1,6,2,2,7].

Follow up: Can you come up with an algorithm that runs in O(n log n) time complexity?''',
        'medium', 'dynamic-programming',
        [
            {
                'input': 'nums = [10,9,2,5,3,7,101,18]',
                'output': '4',
                'explanation': 'The longest increasing subsequence is [2,3,7,18], therefore the length is 4.'
            },
            {
                'input': 'nums = [0,1,0,3,2,3]',
                'output': '4',
                'explanation': 'The longest increasing subsequence is [0,1,2,3], therefore the length is 4.'
            },
            {
                'input': 'nums = [7,7,7,7,7,7,7]',
                'output': '1',
                'explanation': 'All elements are the same, so the longest strictly increasing subsequence has length 1.'
            }
        ],
        [
            '💡 Use dynamic programming: dp[i] represents the length of the longest increasing subsequence ending at index i. For each element, check all previous elements.',
            '💡 For the O(n log n) solution, maintain an array that stores the smallest ending element of all increasing subsequences of length i+1 in tails[i].',
            '💡 Use binary search to find the position where the current element should be placed in the tails array. This gives you the O(n log n) complexity.'
        ],
        [
            '1 ≤ nums.length ≤ 2500',
            '-10⁴ ≤ nums[i] ≤ 10⁴'
        ],
        ['Array', 'Binary Search', 'Dynamic Programming']
    ),
    
    # GRAPHS PROBLEMS
    create_problem(
        'course_schedule', 'Course Schedule',
        '''There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

This problem is essentially asking whether the course dependency graph has a cycle.''',
        'medium', 'graphs',
        [
            {
                'input': 'numCourses = 2, prerequisites = [[1,0]]',
                'output': 'true',
                'explanation': 'There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible.'
            },
            {
                'input': 'numCourses = 2, prerequisites = [[1,0],[0,1]]',
                'output': 'false',
                'explanation': 'There are a total of 2 courses to take. To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.'
            },
            {
                'input': 'numCourses = 3, prerequisites = [[1,0],[2,1]]',
                'output': 'true',
                'explanation': 'Take course 0, then course 1, then course 2. All courses can be completed in this order.'
            }
        ],
        [
            '💡 This is a cycle detection problem in a directed graph. Use DFS with three states: unvisited (0), visiting (1), and visited (2).',
            '💡 Alternative approach: Use topological sorting with Kahn\'s algorithm. If you can process all nodes, there\'s no cycle.',
            '💡 Build an adjacency list from the prerequisites, then perform DFS from each unvisited node to detect back edges (cycles).'
        ],
        [
            '1 ≤ numCourses ≤ 2000',
            '0 ≤ prerequisites.length ≤ 5000',
            'prerequisites[i].length == 2',
            '0 ≤ ai, bi < numCourses',
            'All the pairs prerequisites[i] are unique'
        ],
        ['Depth-First Search', 'Breadth-First Search', 'Graph', 'Topological Sort']
    ),
    
    # TREES PROBLEMS
    create_problem(
        'serialize_deserialize_binary_tree', 'Serialize and Deserialize Binary Tree',
        '''Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.''',
        'hard', 'trees',
        [
            {
                'input': 'root = [1,2,3,null,null,4,5]',
                'output': '[1,2,3,null,null,4,5]',
                'explanation': 'The tree is serialized to a string, then deserialized back to the same tree structure.'
            },
            {
                'input': 'root = []',
                'output': '[]',
                'explanation': 'Empty tree serializes to empty string and deserializes back to empty tree.'
            },
            {
                'input': 'root = [1,2]',
                'output': '[1,2]',
                'explanation': 'Simple tree with root and left child.'
            }
        ],
        [
            '💡 Use preorder traversal for serialization. Include null markers for missing nodes. For deserialization, use the same preorder pattern.',
            '💡 Alternative: Use level-order traversal (BFS) for serialization. This matches LeetCode\'s format but requires handling null nodes carefully.',
            '💡 Consider using a delimiter (like comma) to separate values and a special marker (like "null" or "#") for null nodes.'
        ],
        [
            'The number of nodes in the tree is in the range [0, 10⁴]',
            '-1000 ≤ Node.val ≤ 1000'
        ],
        ['String', 'Tree', 'Depth-First Search', 'Breadth-First Search', 'Design', 'Binary Tree']
    )
]

def save_problems_to_redis(problems):
    """Save all problems to Redis database"""
    success_count = 0
    
    for problem in problems:
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
                tag_key = tag.lower().replace(" ", "_").replace("(", "").replace(")", "")
                redis_client.sadd(f'problems_by_tag:{tag_key}', problem['id'])
            
            success_count += 1
            print(f"✅ Saved '{problem['title']}'")
            
        except Exception as e:
            print(f"❌ Error saving '{problem['title']}': {e}")
    
    return success_count

def main():
    print("🚀 Creating production-ready problems with comprehensive details...")
    
    # Test Redis connection
    try:
        redis_client.ping()
        print("✅ Redis connection successful!")
    except Exception as e:
        print(f"❌ Redis connection failed: {str(e)}")
        return
    
    # Save all problems
    success_count = save_problems_to_redis(production_problems)
    
    print(f"\n🎉 Successfully created {success_count}/{len(production_problems)} production-ready problems!")
    
    # Show summary
    topics = {}
    difficulties = {}
    total_tags = set()
    
    for problem in production_problems:
        topic = problem['topic']
        difficulty = problem['difficulty']
        tags = json.loads(problem['tags'])
        
        topics[topic] = topics.get(topic, 0) + 1
        difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
        total_tags.update(tags)
    
    print(f"\n📊 Problem Distribution:")
    print(f"   Topics: {dict(topics)}")
    print(f"   Difficulties: {dict(difficulties)}")
    print(f"   Total unique tags: {len(total_tags)}")
    
    print(f"\n🏆 Production Features:")
    print(f"   ✓ Comprehensive problem descriptions")
    print(f"   ✓ 3 detailed examples with explanations per problem")
    print(f"   ✓ 3 progressive hints per problem")
    print(f"   ✓ Realistic constraints")
    print(f"   ✓ LeetCode-style tags")
    print(f"   ✓ Challenge-winning quality")
    print(f"   ✓ Production-ready Redis storage")

if __name__ == "__main__":
    main()
