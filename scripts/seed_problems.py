import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    password=os.getenv('REDIS_PASSWORD', ''),
    decode_responses=True
)

def generate_comprehensive_problems():
    problems = []
    
    # Arrays Problems
    array_problems = [
        {
            'id': 'two_sum',
            'title': 'Two Sum',
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'examples': [{'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]'}],
            'constraints': ['2 <= nums.length <= 10^4', '-10^9 <= nums[i] <= 10^9'],
            'hints': ['Use a hash map to store complements', 'One pass solution exists'],
            'difficulty': 'easy',
            'topic': 'arrays',
            'companies': ['Google', 'Amazon', 'Microsoft'],
            'leetcode_url': 'https://leetcode.com/problems/two-sum/',
            'solution_template': 'def twoSum(self, nums, target):\n    # Your solution here\n    pass'
        },
        {
            'id': 'three_sum',
            'title': '3Sum',
            'description': 'Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.',
            'examples': [{'input': 'nums = [-1,0,1,2,-1,-4]', 'output': '[[-1,-1,2],[-1,0,1]]'}],
            'constraints': ['3 <= nums.length <= 3000', '-10^5 <= nums[i] <= 10^5'],
            'hints': ['Sort the array first', 'Use two pointers technique'],
            'difficulty': 'medium',
            'topic': 'arrays',
            'companies': ['Facebook', 'Apple', 'Netflix'],
            'leetcode_url': 'https://leetcode.com/problems/3sum/',
            'solution_template': 'def threeSum(self, nums):\n    # Your solution here\n    pass'
        },
        {
            'id': 'container_water',
            'title': 'Container With Most Water',
            'description': 'You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container that contains the most water.',
            'examples': [{'input': 'height = [1,8,6,2,5,4,8,3,7]', 'output': '49'}],
            'constraints': ['n >= 2', '0 <= height[i] <= 3 * 10^4'],
            'hints': ['Two pointers approach', 'Move the pointer with smaller height'],
            'difficulty': 'medium',
            'topic': 'arrays',
            'companies': ['Amazon', 'Google', 'Microsoft'],
            'leetcode_url': 'https://leetcode.com/problems/container-with-most-water/',
            'solution_template': 'def maxArea(self, height):\n    # Your solution here\n    pass'
        }
    ]
    
    # String Problems
    string_problems = [
        {
            'id': 'longest_substring',
            'title': 'Longest Substring Without Repeating Characters',
            'description': 'Given a string s, find the length of the longest substring without repeating characters.',
            'examples': [{'input': 's = "abcabcbb"', 'output': '3'}],
            'constraints': ['0 <= s.length <= 5 * 10^4'],
            'hints': ['Use sliding window technique', 'Keep track of character positions'],
            'difficulty': 'medium',
            'topic': 'strings',
            'companies': ['Amazon', 'Google', 'Microsoft'],
            'leetcode_url': 'https://leetcode.com/problems/longest-substring-without-repeating-characters/',
            'solution_template': 'def lengthOfLongestSubstring(self, s):\n    # Your solution here\n    pass'
        },
        {
            'id': 'valid_anagram',
            'title': 'Valid Anagram',
            'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.',
            'examples': [{'input': 's = "anagram", t = "nagaram"', 'output': 'true'}],
            'constraints': ['1 <= s.length, t.length <= 5 * 10^4'],
            'hints': ['Count character frequencies', 'Sort both strings'],
            'difficulty': 'easy',
            'topic': 'strings',
            'companies': ['Facebook', 'Amazon', 'Google'],
            'leetcode_url': 'https://leetcode.com/problems/valid-anagram/',
            'solution_template': 'def isAnagram(self, s, t):\n    # Your solution here\n    pass'
        }
    ]
    
    # Tree Problems
    tree_problems = [
        {
            'id': 'max_depth_binary_tree',
            'title': 'Maximum Depth of Binary Tree',
            'description': 'Given the root of a binary tree, return its maximum depth.',
            'examples': [{'input': 'root = [3,9,20,null,null,15,7]', 'output': '3'}],
            'constraints': ['The number of nodes is in the range [0, 10^4]'],
            'hints': ['Use recursion', 'DFS approach'],
            'difficulty': 'easy',
            'topic': 'trees',
            'companies': ['Google', 'Amazon', 'Microsoft'],
            'leetcode_url': 'https://leetcode.com/problems/maximum-depth-of-binary-tree/',
            'solution_template': 'def maxDepth(self, root):\n    # Your solution here\n    pass'
        },
        {
            'id': 'validate_bst',
            'title': 'Validate Binary Search Tree',
            'description': 'Given the root of a binary tree, determine if it is a valid binary search tree (BST).',
            'examples': [{'input': 'root = [2,1,3]', 'output': 'true'}],
            'constraints': ['The number of nodes is in the range [1, 10^4]'],
            'hints': ['Use inorder traversal', 'Keep track of min and max bounds'],
            'difficulty': 'medium',
            'topic': 'trees',
            'companies': ['Facebook', 'Amazon', 'Microsoft'],
            'leetcode_url': 'https://leetcode.com/problems/validate-binary-search-tree/',
            'solution_template': 'def isValidBST(self, root):\n    # Your solution here\n    pass'
        }
    ]
    
    # Dynamic Programming Problems
    dp_problems = [
        {
            'id': 'climbing_stairs',
            'title': 'Climbing Stairs',
            'description': 'You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?',
            'examples': [{'input': 'n = 2', 'output': '2'}, {'input': 'n = 3', 'output': '3'}],
            'constraints': ['1 <= n <= 45'],
            'hints': ['This is a Fibonacci sequence problem', 'Use dynamic programming'],
            'difficulty': 'easy',
            'topic': 'dynamic-programming',
            'companies': ['Amazon', 'Google', 'Microsoft'],
            'leetcode_url': 'https://leetcode.com/problems/climbing-stairs/',
            'solution_template': 'def climbStairs(self, n):\n    # Your solution here\n    pass'
        },
        {
            'id': 'house_robber',
            'title': 'House Robber',
            'description': 'You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. Adjacent houses have security systems connected.',
            'examples': [{'input': 'nums = [1,2,3,1]', 'output': '4'}],
            'constraints': ['1 <= nums.length <= 100', '0 <= nums[i] <= 400'],
            'hints': ['Dynamic programming approach', 'Keep track of max money at each house'],
            'difficulty': 'medium',
            'topic': 'dynamic-programming',
            'companies': ['Amazon', 'Google', 'Apple'],
            'leetcode_url': 'https://leetcode.com/problems/house-robber/',
            'solution_template': 'def rob(self, nums):\n    # Your solution here\n    pass'
        }
    ]
    
    problems.extend(array_problems)
    problems.extend(string_problems)
    problems.extend(tree_problems)
    problems.extend(dp_problems)
    
    # Generate more problems programmatically
    topics = ['arrays', 'strings', 'linked-lists', 'trees', 'graphs', 'dynamic-programming', 'stacks', 'queues', 'heaps', 'hash-tables', 'sorting', 'searching', 'backtracking', 'greedy', 'bit-manipulation']
    difficulties = ['easy', 'medium', 'hard']
    companies = ['Google', 'Amazon', 'Microsoft', 'Apple', 'Facebook', 'Netflix', 'Uber', 'Airbnb', 'LinkedIn', 'Twitter', 'ByteDance', 'Tesla', 'Stripe', 'Dropbox', 'Spotify']
    
    problem_templates = {
        'arrays': 'Find/manipulate elements in an array efficiently',
        'strings': 'Process and analyze string patterns',
        'linked-lists': 'Navigate and modify linked list structures',
        'trees': 'Traverse and analyze tree structures',
        'graphs': 'Find paths and connections in graphs',
        'dynamic-programming': 'Optimize recursive solutions using memoization',
        'stacks': 'Use LIFO data structure for problem solving',
        'queues': 'Use FIFO data structure for problem solving',
        'heaps': 'Maintain priority-based data structures',
        'hash-tables': 'Use key-value mappings for fast lookups',
        'sorting': 'Arrange data in specific order',
        'searching': 'Find elements efficiently in data structures',
        'backtracking': 'Explore all possible solutions systematically',
        'greedy': 'Make locally optimal choices',
        'bit-manipulation': 'Use bitwise operations for optimization'
    }
    
    for topic in topics:
        for difficulty in difficulties:
            count = 70 if difficulty == 'easy' else 60 if difficulty == 'medium' else 40
            for i in range(count):
                problem_id = f'{topic}_{difficulty}_{i+1:03d}'
                problem = {
                    'id': problem_id,
                    'title': f'{topic.replace("-", " ").title()} Challenge {i+1}',
                    'description': f'{problem_templates[topic]}. This {difficulty} level problem tests your understanding of {topic.replace("-", " ")} concepts.',
                    'examples': [
                        {'input': f'Example input for {topic}', 'output': f'Expected output', 'explanation': f'Explanation of the solution approach'}
                    ],
                    'constraints': [f'Standard {difficulty} level constraints', f'Optimized solution expected'],
                    'hints': [f'Consider {topic.replace("-", " ")} properties', f'Think about time complexity', 'Handle edge cases'],
                    'difficulty': difficulty,
                    'topic': topic,
                    'companies': companies[i % len(companies):i % len(companies) + 3],
                    'leetcode_url': f'https://leetcode.com/problems/{problem_id.replace("_", "-")}/',
                    'solution_template': f'def solve(self, input_data):\n    # Solve this {topic} problem\n    # Time: O(?), Space: O(?)\n    pass'
                }
                problems.append(problem)
    
    return problems

def seed_problems():
    print("🚀 Starting problem seeding process...")
    
    problems = generate_comprehensive_problems()
    
    print(f"📊 Generated {len(problems)} problems")
    
    # Clear existing data
    for key in redis_client.scan_iter(match="problem:*"):
        redis_client.delete(key)
    for key in redis_client.scan_iter(match="problems:*"):
        redis_client.delete(key)
    
    redis_client.delete('topics', 'difficulties', 'companies')
    
    # Seed problems
    for i, problem in enumerate(problems):
        problem_key = f"problem:{problem['id']}"
        redis_client.hset(problem_key, mapping={k: json.dumps(v) if isinstance(v, (list, dict)) else str(v) for k, v in problem.items()})
        
        # Add to topic/difficulty indexes
        topic_difficulty_key = f"problems:{problem['difficulty']}:{problem['topic']}"
        redis_client.zadd(topic_difficulty_key, {problem['id']: i})
        
        # Add to sets for filtering
        redis_client.sadd('topics', problem['topic'])
        redis_client.sadd('difficulties', problem['difficulty'])
        redis_client.sadd('companies', *problem['companies'])
        
        if (i + 1) % 100 == 0:
            print(f"✅ Seeded {i + 1} problems...")
    
    # Create summary stats
    stats = {
        'total_problems': len(problems),
        'topics': len(redis_client.smembers('topics')),
        'difficulties': len(redis_client.smembers('difficulties')),
        'companies': len(redis_client.smembers('companies'))
    }
    
    redis_client.hset('platform_stats', mapping=stats)
    
    print(f"""
🎉 Problem seeding completed successfully!

📈 Statistics:
   • Total Problems: {stats['total_problems']}
   • Topics: {stats['topics']}
   • Difficulty Levels: {stats['difficulties']}
   • Companies: {stats['companies']}

🏷️  Topics: {', '.join(sorted(redis_client.smembers('topics')))}
🎯 Difficulties: {', '.join(sorted(redis_client.smembers('difficulties')))}
    """)

if __name__ == "__main__":
    seed_problems()
