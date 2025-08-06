#!/usr/bin/env python3
"""
Create comprehensive problem statements with proper descriptions, examples, constraints
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

def create_problem(id, title, description, difficulty, topic, examples, hints, constraints):
    return {
        'id': id,
        'title': title,
        'description': description,
        'difficulty': difficulty,
        'topic': topic,
        'examples': json.dumps(examples),
        'hints': json.dumps(hints),
        'constraints': json.dumps(constraints),
        'tags': json.dumps([topic.title().replace('-', ' ')])
    }

# Comprehensive problem set with detailed descriptions
comprehensive_problems = [
    # ARRAYS PROBLEMS
    create_problem(
        'two_sum', 'Two Sum',
        '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Follow-up: Can you come up with an algorithm that is less than O(n²) time complexity?''',
        'easy', 'arrays',
        [
            {
                'input': 'nums = [2,7,11,15], target = 9',
                'output': '[0,1]',
                'explanation': 'Because nums[0] + nums[1] = 2 + 7 = 9, we return [0, 1].'
            },
            {
                'input': 'nums = [3,2,4], target = 6',
                'output': '[1,2]',
                'explanation': 'Because nums[1] + nums[2] = 2 + 4 = 6, we return [1, 2].'
            },
            {
                'input': 'nums = [3,3], target = 6',
                'output': '[0,1]',
                'explanation': 'Because nums[0] + nums[1] = 3 + 3 = 6, we return [0, 1].'
            }
        ],
        [
            'A brute force approach would be to check every pair of numbers, but can you do better than O(n²)?',
            'Try using a hash map to store numbers you\'ve already seen along with their indices.',
            'For each number, check if (target - current_number) exists in your hash map.'
        ],
        [
            '2 ≤ nums.length ≤ 10⁴',
            '-10⁹ ≤ nums[i] ≤ 10⁹',
            '-10⁹ ≤ target ≤ 10⁹',
            'Only one valid answer exists.'
        ]
    ),
    
    create_problem(
        'best_time_buy_sell_stock', 'Best Time to Buy and Sell Stock',
        '''You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Note: You must buy before you sell.''',
        'easy', 'arrays',
        [
            {
                'input': 'prices = [7,1,5,3,6,4]',
                'output': '5',
                'explanation': 'Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5. Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.'
            },
            {
                'input': 'prices = [7,6,4,3,1]',
                'output': '0',
                'explanation': 'In this case, no transactions are done and the max profit = 0.'
            },
            {
                'input': 'prices = [1,2,3,4,5]',
                'output': '4',
                'explanation': 'Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.'
            }
        ],
        [
            'Think about tracking the minimum price seen so far as you iterate through the array.',
            'For each day, calculate the profit if you sell on that day (current price - minimum price so far).',
            'Keep track of the maximum profit seen so far.'
        ],
        [
            '1 ≤ prices.length ≤ 10⁵',
            '0 ≤ prices[i] ≤ 10⁴'
        ]
    ),
    
    create_problem(
        'contains_duplicate', 'Contains Duplicate',
        '''Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

This is a fundamental problem that tests your understanding of hash tables and set data structures.''',
        'easy', 'arrays',
        [
            {
                'input': 'nums = [1,2,3,1]',
                'output': 'true',
                'explanation': 'The element 1 appears at index 0 and 3.'
            },
            {
                'input': 'nums = [1,2,3,4]',
                'output': 'false',
                'explanation': 'All elements are distinct.'
            },
            {
                'input': 'nums = [1,1,1,3,3,4,3,2,4,2]',
                'output': 'true',
                'explanation': 'Multiple elements appear more than once.'
            }
        ],
        [
            'Use a hash set to keep track of elements you\'ve already seen.',
            'If you encounter an element that\'s already in the set, return true.',
            'If you finish iterating through the array without finding duplicates, return false.'
        ],
        [
            '1 ≤ nums.length ≤ 10⁵',
            '-10⁹ ≤ nums[i] ≤ 10⁹'
        ]
    ),
    
    create_problem(
        'maximum_subarray', 'Maximum Subarray (Kadane\'s Algorithm)',
        '''Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

This problem is famous for Kadane's algorithm, which solves it in O(n) time and O(1) space.

Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.''',
        'medium', 'arrays',
        [
            {
                'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]',
                'output': '6',
                'explanation': 'The subarray [4,-1,2,1] has the largest sum = 6.'
            },
            {
                'input': 'nums = [1]',
                'output': '1',
                'explanation': 'The subarray is [1] which has the largest sum = 1.'
            },
            {
                'input': 'nums = [5,4,-1,7,8]',
                'output': '23',
                'explanation': 'The subarray [5,4,-1,7,8] has the largest sum = 23.'
            }
        ],
        [
            'Try using Kadane\'s algorithm - keep track of the maximum sum ending at each position.',
            'At each position, decide whether to extend the existing subarray or start a new one.',
            'The key insight: if the sum so far becomes negative, it\'s better to start fresh from the current element.'
        ],
        [
            '1 ≤ nums.length ≤ 10⁵',
            '-10⁴ ≤ nums[i] ≤ 10⁴'
        ]
    ),
    
    # STRINGS PROBLEMS
    create_problem(
        'valid_anagram', 'Valid Anagram',
        '''Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?''',
        'easy', 'strings',
        [
            {
                'input': 's = "anagram", t = "nagaram"',
                'output': 'true',
                'explanation': 'Both strings contain the same characters with the same frequency.'
            },
            {
                'input': 's = "rat", t = "car"',
                'output': 'false',
                'explanation': 'The strings contain different characters.'
            },
            {
                'input': 's = "a", t = "ab"',
                'output': 'false',
                'explanation': 'The strings have different lengths, so they cannot be anagrams.'
            }
        ],
        [
            'Count the frequency of each character in both strings and compare.',
            'Alternatively, sort both strings and check if they are equal.',
            'Consider the time and space complexity of each approach.'
        ],
        [
            '1 ≤ s.length, t.length ≤ 5 × 10⁴',
            's and t consist of lowercase English letters'
        ]
    ),
    
    create_problem(
        'valid_palindrome', 'Valid Palindrome',
        '''A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.''',
        'easy', 'strings',
        [
            {
                'input': 's = "A man, a plan, a canal: Panama"',
                'output': 'true',
                'explanation': 'After processing: "amanaplanacanalpanama" is a palindrome.'
            },
            {
                'input': 's = "race a car"',
                'output': 'false',
                'explanation': 'After processing: "raceacar" is not a palindrome.'
            },
            {
                'input': 's = " "',
                'output': 'true',
                'explanation': 'After removing non-alphanumeric characters, the string becomes empty, which is considered a palindrome.'
            }
        ],
        [
            'Use two pointers, one from the beginning and one from the end of the string.',
            'Skip non-alphanumeric characters and compare characters after converting to lowercase.',
            'Move the pointers towards each other until they meet or cross.'
        ],
        [
            '1 ≤ s.length ≤ 2 × 10⁵',
            's consists only of printable ASCII characters'
        ]
    ),
    
    # LINKED LISTS PROBLEMS
    create_problem(
        'reverse_linked_list', 'Reverse Linked List',
        '''Given the head of a singly linked list, reverse the list, and return the reversed list.

This is a fundamental linked list problem that tests your understanding of pointer manipulation.

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?''',
        'easy', 'linked-lists',
        [
            {
                'input': 'head = [1,2,3,4,5]',
                'output': '[5,4,3,2,1]',
                'explanation': 'The linked list 1->2->3->4->5 becomes 5->4->3->2->1.'
            },
            {
                'input': 'head = [1,2]',
                'output': '[2,1]',
                'explanation': 'The linked list 1->2 becomes 2->1.'
            },
            {
                'input': 'head = []',
                'output': '[]',
                'explanation': 'Empty list remains empty after reversal.'
            }
        ],
        [
            'Use three pointers: previous, current, and next to keep track of nodes.',
            'Iteratively reverse the links between consecutive nodes.',
            'Handle the edge cases of empty list and single node list.'
        ],
        [
            'The number of nodes in the list is the range [0, 5000]',
            '-5000 ≤ Node.val ≤ 5000'
        ]
    ),
    
    # TREES PROBLEMS
    create_problem(
        'maximum_depth_binary_tree', 'Maximum Depth of Binary Tree',
        '''Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

This problem can be solved using both recursive and iterative approaches.''',
        'easy', 'trees',
        [
            {
                'input': 'root = [3,9,20,null,null,15,7]',
                'output': '3',
                'explanation': 'The maximum depth is 3, following the path 3 -> 20 -> 7 or 3 -> 20 -> 15.'
            },
            {
                'input': 'root = [1,null,2]',
                'output': '2',
                'explanation': 'The maximum depth is 2, following the path 1 -> 2.'
            },
            {
                'input': 'root = []',
                'output': '0',
                'explanation': 'Empty tree has depth 0.'
            }
        ],
        [
            'Think recursively: the depth of a tree is 1 + max(depth of left subtree, depth of right subtree).',
            'Base case: if the node is null, return 0.',
            'You can also solve this iteratively using BFS (level-order traversal).'
        ],
        [
            'The number of nodes in the tree is in the range [0, 10⁴]',
            '-100 ≤ Node.val ≤ 100'
        ]
    )
]

print("Testing Redis connection...")
try:
    redis_client.ping()
    print("✅ Redis connection successful!")
except Exception as e:
    print(f"❌ Redis connection failed: {str(e)}")
    exit(1)

print("Initializing comprehensive problems...")
for problem in comprehensive_problems:
    # Store problem data
    redis_client.hset(f"problem:{problem['id']}", mapping=problem)
    
    # Add to difficulty-topic sorted set
    redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
    
    # Add to topics and difficulties sets
    redis_client.sadd('topics', problem['topic'])
    redis_client.sadd('difficulties', problem['difficulty'])

print(f"✅ {len(comprehensive_problems)} comprehensive problems initialized!")

# Show sample problem
sample_problem = comprehensive_problems[0]
print(f"\n📋 Sample Problem: {sample_problem['title']}")
print(f"Description length: {len(sample_problem['description'])} characters")
examples = json.loads(sample_problem['examples'])
print(f"Examples: {len(examples)} detailed examples")
hints = json.loads(sample_problem['hints'])
print(f"Hints: {len(hints)} progressive hints")
constraints = json.loads(sample_problem['constraints'])
print(f"Constraints: {len(constraints)} specific constraints")

print("\n🎉 Comprehensive problem initialization complete!")
print("Each problem now includes:")
print("   • Detailed problem description with context")
print("   • 3 comprehensive examples with explanations")
print("   • 3 progressive hints")
print("   • Specific constraints")
print("   • Proper input/output format")
print("   • Follow-up questions where applicable")
