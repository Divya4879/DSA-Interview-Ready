#!/usr/bin/env python3
"""
Create High-Quality DSA Problems for Redis AI Challenge
Real interview problems with detailed descriptions, test cases, and constraints
"""

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

def create_quality_problems():
    """Create detailed, real DSA interview problems"""
    
    problems = [
        {
            'id': 'two_sum',
            'title': 'Two Sum',
            'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.''',
            'examples': [
                {
                    'input': 'nums = [2,7,11,15], target = 9',
                    'output': '[0,1]',
                    'explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1].'
                },
                {
                    'input': 'nums = [3,2,4], target = 6',
                    'output': '[1,2]',
                    'explanation': 'Because nums[1] + nums[2] == 6, we return [1, 2].'
                },
                {
                    'input': 'nums = [3,3], target = 6',
                    'output': '[0,1]',
                    'explanation': 'Because nums[0] + nums[1] == 6, we return [0, 1].'
                }
            ],
            'constraints': [
                '2 ≤ nums.length ≤ 10⁴',
                '-10⁹ ≤ nums[i] ≤ 10⁹',
                '-10⁹ ≤ target ≤ 10⁹',
                'Only one valid answer exists.'
            ],
            'hints': [
                'A really brute force way would be to search for all possible pairs of numbers but that would be too slow. Again, it\'s best to try out brute force solutions for just for completeness. It is from these brute force solutions that you can come up with optimizations.',
                'So, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y which is value - x where value is the input parameter. Can we change our array somehow so that this search becomes faster?',
                'The second train of thought is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?'
            ],
            'difficulty': 'easy',
            'topic': 'arrays',
            'companies': ['Amazon', 'Google', 'Microsoft', 'Facebook', 'Apple'],
            'leetcode_url': 'https://leetcode.com/problems/two-sum/',
            'solution_template': '''def twoSum(self, nums: List[int], target: int) -> List[int]:
    # Approach 1: Brute Force - O(n²) time, O(1) space
    # Approach 2: Hash Map - O(n) time, O(n) space
    
    # Your solution here
    pass''',
            'test_cases': [
                {'input': {'nums': [2, 7, 11, 15], 'target': 9}, 'expected': [0, 1]},
                {'input': {'nums': [3, 2, 4], 'target': 6}, 'expected': [1, 2]},
                {'input': {'nums': [3, 3], 'target': 6}, 'expected': [0, 1]},
                {'input': {'nums': [-1, -2, -3, -4, -5], 'target': -8}, 'expected': [2, 4]},
                {'input': {'nums': [0, 4, 3, 0], 'target': 0}, 'expected': [0, 3]}
            ],
            'time_complexity': 'O(n) with hash map approach',
            'space_complexity': 'O(n) for hash map storage'
        },
        
        {
            'id': 'valid_parentheses',
            'title': 'Valid Parentheses',
            'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.''',
            'examples': [
                {
                    'input': 's = "()"',
                    'output': 'true',
                    'explanation': 'The string contains valid parentheses pairs.'
                },
                {
                    'input': 's = "()[]{}"',
                    'output': 'true',
                    'explanation': 'All brackets are properly matched and nested.'
                },
                {
                    'input': 's = "(]"',
                    'output': 'false',
                    'explanation': 'Mismatched bracket types.'
                },
                {
                    'input': 's = "([)]"',
                    'output': 'false',
                    'explanation': 'Brackets are not properly nested.'
                }
            ],
            'constraints': [
                '1 ≤ s.length ≤ 10⁴',
                's consists of parentheses only \'()[]{}\''
            ],
            'hints': [
                'Use a stack data structure to keep track of opening brackets.',
                'When you encounter a closing bracket, check if it matches the most recent opening bracket.',
                'If the stack is empty at the end, all brackets were properly matched.'
            ],
            'difficulty': 'easy',
            'topic': 'stacks',
            'companies': ['Amazon', 'Microsoft', 'Google', 'Facebook'],
            'leetcode_url': 'https://leetcode.com/problems/valid-parentheses/',
            'solution_template': '''def isValid(self, s: str) -> bool:
    # Use stack to track opening brackets
    # Time: O(n), Space: O(n)
    
    # Your solution here
    pass''',
            'test_cases': [
                {'input': {'s': '()'}, 'expected': True},
                {'input': {'s': '()[]{}'}, 'expected': True},
                {'input': {'s': '(]'}, 'expected': False},
                {'input': {'s': '([)]'}, 'expected': False},
                {'input': {'s': '{[]}'}, 'expected': True},
                {'input': {'s': ''}, 'expected': True},
                {'input': {'s': '((('}, 'expected': False}
            ],
            'time_complexity': 'O(n) where n is length of string',
            'space_complexity': 'O(n) for stack storage'
        },
        
        {
            'id': 'maximum_subarray',
            'title': 'Maximum Subarray (Kadane\'s Algorithm)',
            'description': '''Given an integer array nums, find the subarray with the largest sum, and return its sum.

A subarray is a contiguous non-empty sequence of elements within an array.''',
            'examples': [
                {
                    'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
                    'output': '6',
                    'explanation': 'The subarray [4,-1,2,1] has the largest sum 6.'
                },
                {
                    'input': 'nums = [1]',
                    'output': '1',
                    'explanation': 'The subarray [1] has the largest sum 1.'
                },
                {
                    'input': 'nums = [5,4,-1,7,8]',
                    'output': '23',
                    'explanation': 'The subarray [5,4,-1,7,8] has the largest sum 23.'
                }
            ],
            'constraints': [
                '1 ≤ nums.length ≤ 10⁵',
                '-10⁴ ≤ nums[i] ≤ 10⁴'
            ],
            'hints': [
                'Try using dynamic programming. At each position, decide whether to start a new subarray or extend the existing one.',
                'Keep track of the maximum sum seen so far and the maximum sum ending at the current position.',
                'This is a classic application of Kadane\'s algorithm.'
            ],
            'difficulty': 'medium',
            'topic': 'dynamic-programming',
            'companies': ['Amazon', 'Microsoft', 'Google', 'Apple', 'Netflix'],
            'leetcode_url': 'https://leetcode.com/problems/maximum-subarray/',
            'solution_template': '''def maxSubArray(self, nums: List[int]) -> int:
    # Kadane's Algorithm
    # Time: O(n), Space: O(1)
    
    # Your solution here
    pass''',
            'test_cases': [
                {'input': {'nums': [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, 'expected': 6},
                {'input': {'nums': [1]}, 'expected': 1},
                {'input': {'nums': [5, 4, -1, 7, 8]}, 'expected': 23},
                {'input': {'nums': [-1]}, 'expected': -1},
                {'input': {'nums': [-2, -1]}, 'expected': -1}
            ],
            'time_complexity': 'O(n) single pass through array',
            'space_complexity': 'O(1) constant extra space'
        },
        
        {
            'id': 'binary_tree_inorder',
            'title': 'Binary Tree Inorder Traversal',
            'description': '''Given the root of a binary tree, return the inorder traversal of its nodes' values.

Inorder traversal visits nodes in the order: Left → Root → Right

Follow up: Recursive solution is trivial, could you do it iteratively?''',
            'examples': [
                {
                    'input': 'root = [1,null,2,3]',
                    'output': '[1,3,2]',
                    'explanation': '''Tree structure:
   1
    \\
     2
    /
   3
Inorder: Left(none) → Root(1) → Right(2)
For node 2: Left(3) → Root(2) → Right(none)
Result: [1,3,2]'''
                },
                {
                    'input': 'root = []',
                    'output': '[]',
                    'explanation': 'Empty tree returns empty list.'
                },
                {
                    'input': 'root = [1]',
                    'output': '[1]',
                    'explanation': 'Single node tree returns [1].'
                }
            ],
            'constraints': [
                'The number of nodes in the tree is in the range [0, 100]',
                '-100 ≤ Node.val ≤ 100'
            ],
            'hints': [
                'For recursive approach: process left subtree, current node, then right subtree.',
                'For iterative approach: use a stack to simulate the recursion.',
                'Go as far left as possible, then process nodes and move right.'
            ],
            'difficulty': 'easy',
            'topic': 'trees',
            'companies': ['Microsoft', 'Amazon', 'Google', 'Facebook'],
            'leetcode_url': 'https://leetcode.com/problems/binary-tree-inorder-traversal/',
            'solution_template': '''# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    # Approach 1: Recursive - O(n) time, O(h) space
    # Approach 2: Iterative with stack - O(n) time, O(h) space
    
    # Your solution here
    pass''',
            'test_cases': [
                {'input': {'root': [1, None, 2, 3]}, 'expected': [1, 3, 2]},
                {'input': {'root': []}, 'expected': []},
                {'input': {'root': [1]}, 'expected': [1]},
                {'input': {'root': [1, 2, 3, 4, 5]}, 'expected': [4, 2, 5, 1, 3]}
            ],
            'time_complexity': 'O(n) where n is number of nodes',
            'space_complexity': 'O(h) where h is height of tree'
        },
        
        {
            'id': 'longest_substring_no_repeat',
            'title': 'Longest Substring Without Repeating Characters',
            'description': '''Given a string s, find the length of the longest substring without repeating characters.

A substring is a contiguous non-empty sequence of characters within a string.''',
            'examples': [
                {
                    'input': 's = "abcabcbb"',
                    'output': '3',
                    'explanation': 'The answer is "abc", with the length of 3.'
                },
                {
                    'input': 's = "bbbbb"',
                    'output': '1',
                    'explanation': 'The answer is "b", with the length of 1.'
                },
                {
                    'input': 's = "pwwkew"',
                    'output': '3',
                    'explanation': 'The answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.'
                }
            ],
            'constraints': [
                '0 ≤ s.length ≤ 5 * 10⁴',
                's consists of English letters, digits, symbols and spaces'
            ],
            'hints': [
                'Use the sliding window technique with two pointers.',
                'Keep track of characters in the current window using a hash set or hash map.',
                'When you find a repeating character, shrink the window from the left.'
            ],
            'difficulty': 'medium',
            'topic': 'strings',
            'companies': ['Amazon', 'Microsoft', 'Google', 'Facebook', 'Apple'],
            'leetcode_url': 'https://leetcode.com/problems/longest-substring-without-repeating-characters/',
            'solution_template': '''def lengthOfLongestSubstring(self, s: str) -> int:
    # Sliding Window with Hash Set
    # Time: O(n), Space: O(min(m,n)) where m is charset size
    
    # Your solution here
    pass''',
            'test_cases': [
                {'input': {'s': 'abcabcbb'}, 'expected': 3},
                {'input': {'s': 'bbbbb'}, 'expected': 1},
                {'input': {'s': 'pwwkew'}, 'expected': 3},
                {'input': {'s': ''}, 'expected': 0},
                {'input': {'s': 'au'}, 'expected': 2},
                {'input': {'s': 'dvdf'}, 'expected': 3}
            ],
            'time_complexity': 'O(n) where n is length of string',
            'space_complexity': 'O(min(m,n)) where m is charset size'
        }
    ]
    
    return problems

def seed_quality_problems():
    """Replace generic problems with high-quality detailed ones"""
    print("🚀 Creating high-quality DSA problems...")
    
    # Clear existing generic problems
    for key in redis_client.scan_iter(match="problem:*"):
        redis_client.delete(key)
    
    problems = create_quality_problems()
    
    for i, problem in enumerate(problems):
        problem_key = f"problem:{problem['id']}"
        
        # Store with proper JSON serialization
        redis_data = {}
        for key, value in problem.items():
            if isinstance(value, (list, dict)):
                redis_data[key] = json.dumps(value)
            else:
                redis_data[key] = str(value)
        
        redis_client.hset(problem_key, mapping=redis_data)
        
        # Add to indexes
        topic_difficulty_key = f"problems:{problem['difficulty']}:{problem['topic']}"
        redis_client.zadd(topic_difficulty_key, {problem['id']: i})
        
        print(f"✅ Created: {problem['title']}")
    
    print(f"\n🎉 Successfully created {len(problems)} high-quality problems!")
    print("\n📋 Problems include:")
    for problem in problems:
        print(f"  • {problem['title']} ({problem['difficulty']}) - {problem['topic']}")
    
    print("\n🔧 Each problem includes:")
    print("  • Detailed problem description")
    print("  • Multiple test cases with explanations") 
    print("  • Comprehensive constraints")
    print("  • Strategic hints")
    print("  • Time/space complexity analysis")
    print("  • Company tags")
    print("  • LeetCode links")

if __name__ == "__main__":
    seed_quality_problems()
