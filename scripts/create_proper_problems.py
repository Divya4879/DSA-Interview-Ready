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

# Comprehensive problem set with proper descriptions
problems = []

# ARRAYS PROBLEMS (10 problems)
arrays_problems = [
    create_problem(
        'two_sum', 'Two Sum',
        'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.',
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
        'You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.',
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
        'Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.',
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
        'product_except_self', 'Product of Array Except Self',
        'Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i]. The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer. You must write an algorithm that runs in O(n) time and without using the division operation.',
        'medium', 'arrays',
        [
            {
                'input': 'nums = [1,2,3,4]',
                'output': '[24,12,8,6]',
                'explanation': 'For index 0: product of [2,3,4] = 24. For index 1: product of [1,3,4] = 12. For index 2: product of [1,2,4] = 8. For index 3: product of [1,2,3] = 6.'
            },
            {
                'input': 'nums = [-1,1,0,-3,3]',
                'output': '[0,0,9,0,0]',
                'explanation': 'Since there\'s a zero in the array, most products will be zero except for the position of the zero itself.'
            },
            {
                'input': 'nums = [2,3,4,5]',
                'output': '[60,40,30,24]',
                'explanation': 'Product of all elements except each position.'
            }
        ],
        [
            'Think about calculating the product of elements to the left and right of each position.',
            'You can use two passes: one to calculate left products, another for right products.',
            'Can you optimize space by using the output array to store intermediate results?'
        ],
        [
            '2 ≤ nums.length ≤ 10⁵',
            '-30 ≤ nums[i] ≤ 30',
            'The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.'
        ]
    ),
    
    create_problem(
        'maximum_subarray', 'Maximum Subarray (Kadane\'s Algorithm)',
        'Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum. A subarray is a contiguous part of an array.',
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
    
    create_problem(
        'find_minimum_rotated_sorted', 'Find Minimum in Rotated Sorted Array',
        'Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2] if it was rotated 4 times. Given the sorted rotated array nums of unique elements, return the minimum element of this array. You must write an algorithm that runs in O(log n) time.',
        'medium', 'arrays',
        [
            {
                'input': 'nums = [3,4,5,1,2]',
                'output': '1',
                'explanation': 'The original array was [1,2,3,4,5] rotated 3 times.'
            },
            {
                'input': 'nums = [4,5,6,7,0,1,2]',
                'output': '0',
                'explanation': 'The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.'
            },
            {
                'input': 'nums = [11,13,15,17]',
                'output': '11',
                'explanation': 'The original array was [11,13,15,17] and it was rotated 4 times (no rotation).'
            }
        ],
        [
            'Use binary search approach since the array is sorted (but rotated).',
            'Compare the middle element with the rightmost element to determine which half is sorted.',
            'The minimum element is where the rotation happened - where a smaller element follows a larger one.'
        ],
        [
            'n == nums.length',
            '1 ≤ n ≤ 5000',
            '-5000 ≤ nums[i] ≤ 5000',
            'All the integers of nums are unique.',
            'nums is sorted and rotated between 1 and n times.'
        ]
    ),
    
    create_problem(
        'search_rotated_sorted', 'Search in Rotated Sorted Array',
        'There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2]. Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums. You must write an algorithm with O(log n) runtime complexity.',
        'medium', 'arrays',
        [
            {
                'input': 'nums = [4,5,6,7,0,1,2], target = 0',
                'output': '4',
                'explanation': 'Target 0 is found at index 4.'
            },
            {
                'input': 'nums = [4,5,6,7,0,1,2], target = 3',
                'output': '-1',
                'explanation': 'Target 3 is not in the array.'
            },
            {
                'input': 'nums = [1], target = 0',
                'output': '-1',
                'explanation': 'Target 0 is not found in the single element array.'
            }
        ],
        [
            'Use modified binary search - the array is sorted but rotated.',
            'At each step, determine which half of the array is properly sorted.',
            'Check if the target lies within the sorted half, then decide which half to search next.'
        ],
        [
            '1 ≤ nums.length ≤ 5000',
            '-10⁴ ≤ nums[i] ≤ 10⁴',
            'All values of nums are unique.',
            'nums is an ascending array that is possibly rotated.',
            '-10⁴ ≤ target ≤ 10⁴'
        ]
    ),
    
    create_problem(
        'three_sum', '3Sum',
        'Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0. Notice that the solution set must not contain duplicate triplets.',
        'medium', 'arrays',
        [
            {
                'input': 'nums = [-1,0,1,2,-1,-4]',
                'output': '[[-1,-1,2],[-1,0,1]]',
                'explanation': 'nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0. nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0. nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0. The distinct triplets are [-1,0,1] and [-1,-1,2].'
            },
            {
                'input': 'nums = [0,1,1]',
                'output': '[]',
                'explanation': 'The only possible triplet does not sum up to 0.'
            },
            {
                'input': 'nums = [0,0,0]',
                'output': '[[0,0,0]]',
                'explanation': 'The only possible triplet sums up to 0.'
            }
        ],
        [
            'Sort the array first to make it easier to avoid duplicates and use two pointers.',
            'For each element, use two pointers technique to find pairs that sum to the negative of that element.',
            'Skip duplicate values to avoid duplicate triplets in the result.'
        ],
        [
            '3 ≤ nums.length ≤ 3000',
            '-10⁵ ≤ nums[i] ≤ 10⁵'
        ]
    ),
    
    create_problem(
        'container_most_water', 'Container With Most Water',
        'You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container that can hold the most water. Return the maximum amount of water a container can store. Notice that you may not slant the container.',
        'medium', 'arrays',
        [
            {
                'input': 'height = [1,8,6,2,5,4,8,3,7]',
                'output': '49',
                'explanation': 'The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.'
            },
            {
                'input': 'height = [1,1]',
                'output': '1',
                'explanation': 'The maximum area is 1.'
            },
            {
                'input': 'height = [1,2,1]',
                'output': '2',
                'explanation': 'The maximum area is formed by the lines at index 0 and 2, with area = min(1,1) * (2-0) = 2.'
            }
        ],
        [
            'Use two pointers starting from both ends of the array.',
            'The area is determined by the shorter line and the distance between the two lines.',
            'Move the pointer with the shorter height inward, as moving the taller one won\'t increase the area.'
        ],
        [
            'n == height.length',
            '2 ≤ n ≤ 10⁵',
            '0 ≤ height[i] ≤ 10⁴'
        ]
    ),
    
    create_problem(
        'merge_intervals', 'Merge Intervals',
        'Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.',
        'medium', 'arrays',
        [
            {
                'input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]',
                'output': '[[1,6],[8,10],[15,18]]',
                'explanation': 'Since intervals [1,3] and [2,6] overlap, merge them into [1,6].'
            },
            {
                'input': 'intervals = [[1,4],[4,5]]',
                'output': '[[1,5]]',
                'explanation': 'Intervals [1,4] and [4,5] are considered overlapping.'
            },
            {
                'input': 'intervals = [[1,4],[2,3]]',
                'output': '[[1,4]]',
                'explanation': 'Interval [2,3] is completely contained within [1,4].'
            }
        ],
        [
            'Sort the intervals by their start times first.',
            'Iterate through the sorted intervals and merge overlapping ones.',
            'Two intervals overlap if the start of the second is less than or equal to the end of the first.'
        ],
        [
            '1 ≤ intervals.length ≤ 10⁴',
            'intervals[i].length == 2',
            '0 ≤ starti ≤ endi ≤ 10⁴'
        ]
    )
]

problems.extend(arrays_problems)
print(f"✅ Created {len(arrays_problems)} comprehensive array problems")

print("Testing Redis connection...")
try:
    redis_client.ping()
    print("✅ Redis connection successful!")
except Exception as e:
    print(f"❌ Redis connection failed: {str(e)}")
    exit(1)

print("Initializing comprehensive problems...")
for problem in problems:
    # Store problem data
    redis_client.hset(f"problem:{problem['id']}", mapping=problem)
    
    # Add to difficulty-topic sorted set
    redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
    
    # Add to topics and difficulties sets
    redis_client.sadd('topics', problem['topic'])
    redis_client.sadd('difficulties', problem['difficulty'])

print(f"✅ {len(problems)} comprehensive problems initialized!")

# Show sample problem
sample_problem = problems[0]
print(f"\n📋 Sample Problem: {sample_problem['title']}")
print(f"Description: {sample_problem['description'][:100]}...")
examples = json.loads(sample_problem['examples'])
print(f"Examples: {len(examples)} detailed examples")
hints = json.loads(sample_problem['hints'])
print(f"Hints: {len(hints)} progressive hints")
constraints = json.loads(sample_problem['constraints'])
print(f"Constraints: {len(constraints)} specific constraints")

print("\n🎉 Comprehensive problem initialization complete!")
print("Each problem now includes:")
print("   • Detailed problem description")
print("   • 3 comprehensive examples with explanations")
print("   • 3 progressive hints")
print("   • Specific constraints")
print("   • Proper input/output format")
