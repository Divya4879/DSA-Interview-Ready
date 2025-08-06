#!/usr/bin/env python3
"""
Generate 80+ DSA problems across 8 topics (10+ problems per topic)
"""

import json

def create_all_problems():
    problems = []
    
    # 1. ARRAYS (10 problems)
    arrays = [
        {
            'id': 'two_sum', 'title': 'Two Sum', 'difficulty': 'easy', 'topic': 'arrays',
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'examples': [
                {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'Because nums[0] + nums[1] = 2 + 7 = 9'},
                {'input': 'nums = [3,2,4], target = 6', 'output': '[1,2]', 'explanation': 'Because nums[1] + nums[2] = 2 + 4 = 6'},
                {'input': 'nums = [3,3], target = 6', 'output': '[0,1]', 'explanation': 'Because nums[0] + nums[1] = 3 + 3 = 6'}
            ],
            'hints': ['Use a hash map to store numbers you\'ve seen', 'For each number, check if its complement exists', 'The complement is target - current_number'],
            'constraints': ['2 ≤ nums.length ≤ 10⁴', '-10⁹ ≤ nums[i] ≤ 10⁹', '-10⁹ ≤ target ≤ 10⁹']
        },
        {
            'id': 'best_time_buy_sell_stock', 'title': 'Best Time to Buy and Sell Stock', 'difficulty': 'easy', 'topic': 'arrays',
            'description': 'You are given an array prices where prices[i] is the price of a given stock on the ith day. Find the maximum profit.',
            'examples': [
                {'input': 'prices = [7,1,5,3,6,4]', 'output': '5', 'explanation': 'Buy on day 2 (price = 1) and sell on day 5 (price = 6)'},
                {'input': 'prices = [7,6,4,3,1]', 'output': '0', 'explanation': 'No transactions are done, max profit = 0'},
                {'input': 'prices = [1,2,3,4,5]', 'output': '4', 'explanation': 'Buy on day 1 and sell on day 5'}
            ],
            'hints': ['Track the minimum price seen so far', 'Calculate profit for each day', 'Keep track of maximum profit'],
            'constraints': ['1 ≤ prices.length ≤ 10⁵', '0 ≤ prices[i] ≤ 10⁴']
        },
        {
            'id': 'contains_duplicate', 'title': 'Contains Duplicate', 'difficulty': 'easy', 'topic': 'arrays',
            'description': 'Given an integer array nums, return true if any value appears at least twice in the array.',
            'examples': [
                {'input': 'nums = [1,2,3,1]', 'output': 'true', 'explanation': 'Element 1 appears twice'},
                {'input': 'nums = [1,2,3,4]', 'output': 'false', 'explanation': 'All elements are distinct'},
                {'input': 'nums = [1,1,1,3,3,4,3,2,4,2]', 'output': 'true', 'explanation': 'Multiple duplicates exist'}
            ],
            'hints': ['Use a hash set to track seen elements', 'Return true if element already exists', 'Return false if no duplicates found'],
            'constraints': ['1 ≤ nums.length ≤ 10⁵', '-10⁹ ≤ nums[i] ≤ 10⁹']
        },
        {
            'id': 'product_except_self', 'title': 'Product of Array Except Self', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].',
            'examples': [
                {'input': 'nums = [1,2,3,4]', 'output': '[24,12,8,6]', 'explanation': 'Product except self for each position'},
                {'input': 'nums = [-1,1,0,-3,3]', 'output': '[0,0,9,0,0]', 'explanation': 'Zero makes most products zero'},
                {'input': 'nums = [2,3,4,5]', 'output': '[60,40,30,24]', 'explanation': 'Product of all other elements'}
            ],
            'hints': ['Think about left and right products', 'Use two passes through the array', 'Can you do it without division?'],
            'constraints': ['2 ≤ nums.length ≤ 10⁵', '-30 ≤ nums[i] ≤ 30']
        },
        {
            'id': 'maximum_subarray', 'title': 'Maximum Subarray', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'Given an integer array nums, find the contiguous subarray with the largest sum and return its sum.',
            'examples': [
                {'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]', 'output': '6', 'explanation': 'Subarray [4,-1,2,1] has the largest sum'},
                {'input': 'nums = [1]', 'output': '1', 'explanation': 'Single element array'},
                {'input': 'nums = [5,4,-1,7,8]', 'output': '23', 'explanation': 'The entire array has the largest sum'}
            ],
            'hints': ['Use Kadane\'s algorithm', 'Decide whether to extend subarray or start new', 'If sum becomes negative, start fresh'],
            'constraints': ['1 ≤ nums.length ≤ 10⁵', '-10⁴ ≤ nums[i] ≤ 10⁴']
        },
        {
            'id': 'find_minimum_rotated_sorted', 'title': 'Find Minimum in Rotated Sorted Array', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'Suppose an array of length n sorted in ascending order is rotated. Find the minimum element.',
            'examples': [
                {'input': 'nums = [3,4,5,1,2]', 'output': '1', 'explanation': 'The original array was [1,2,3,4,5] rotated 3 times'},
                {'input': 'nums = [4,5,6,7,0,1,2]', 'output': '0', 'explanation': 'The original array was [0,1,2,4,5,6,7] rotated 4 times'},
                {'input': 'nums = [11,13,15,17]', 'output': '11', 'explanation': 'The original array was not rotated'}
            ],
            'hints': ['Use binary search approach', 'Compare middle element with right element', 'The minimum is where the rotation happened'],
            'constraints': ['n == nums.length', '1 ≤ n ≤ 5000', '-5000 ≤ nums[i] ≤ 5000']
        },
        {
            'id': 'search_rotated_sorted', 'title': 'Search in Rotated Sorted Array', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'There is an integer array nums sorted in ascending order (with distinct values). Search for target value.',
            'examples': [
                {'input': 'nums = [4,5,6,7,0,1,2], target = 0', 'output': '4', 'explanation': 'Target 0 is at index 4'},
                {'input': 'nums = [4,5,6,7,0,1,2], target = 3', 'output': '-1', 'explanation': 'Target 3 is not in array'},
                {'input': 'nums = [1], target = 0', 'output': '-1', 'explanation': 'Target not found in single element array'}
            ],
            'hints': ['Use modified binary search', 'Determine which half is sorted', 'Check if target is in the sorted half'],
            'constraints': ['1 ≤ nums.length ≤ 5000', '-10⁴ ≤ nums[i] ≤ 10⁴', '-10⁴ ≤ target ≤ 10⁴']
        },
        {
            'id': 'three_sum', 'title': '3Sum', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'Given an integer array nums, return all the triplets that sum to zero.',
            'examples': [
                {'input': 'nums = [-1,0,1,2,-1,-4]', 'output': '[[-1,-1,2],[-1,0,1]]', 'explanation': 'Two triplets sum to zero'},
                {'input': 'nums = [0,1,1]', 'output': '[]', 'explanation': 'No triplets sum to zero'},
                {'input': 'nums = [0,0,0]', 'output': '[[0,0,0]]', 'explanation': 'Only one triplet sums to zero'}
            ],
            'hints': ['Sort the array first', 'Use two pointers technique', 'Skip duplicates to avoid duplicate triplets'],
            'constraints': ['3 ≤ nums.length ≤ 3000', '-10⁵ ≤ nums[i] ≤ 10⁵']
        },
        {
            'id': 'container_most_water', 'title': 'Container With Most Water', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'You are given an integer array height. Find two lines that together with the x-axis form a container that holds the most water.',
            'examples': [
                {'input': 'height = [1,8,6,2,5,4,8,3,7]', 'output': '49', 'explanation': 'Lines at index 1 and 8 form the largest container'},
                {'input': 'height = [1,1]', 'output': '1', 'explanation': 'Only two lines available'},
                {'input': 'height = [1,2,1]', 'output': '2', 'explanation': 'Lines at index 0 and 2 form container of area 2'}
            ],
            'hints': ['Use two pointers from both ends', 'Move the pointer with smaller height', 'Calculate area at each step'],
            'constraints': ['n == height.length', '2 ≤ n ≤ 10⁵', '0 ≤ height[i] ≤ 10⁴']
        },
        {
            'id': 'merge_intervals', 'title': 'Merge Intervals', 'difficulty': 'medium', 'topic': 'arrays',
            'description': 'Given an array of intervals, merge all overlapping intervals.',
            'examples': [
                {'input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]', 'output': '[[1,6],[8,10],[15,18]]', 'explanation': '[1,3] and [2,6] overlap'},
                {'input': 'intervals = [[1,4],[4,5]]', 'output': '[[1,5]]', 'explanation': 'Intervals [1,4] and [4,5] are considered overlapping'},
                {'input': 'intervals = [[1,4],[2,3]]', 'output': '[[1,4]]', 'explanation': '[2,3] is completely inside [1,4]'}
            ],
            'hints': ['Sort intervals by start time', 'Merge overlapping intervals as you go', 'Check if current interval overlaps with the last merged interval'],
            'constraints': ['1 ≤ intervals.length ≤ 10⁴', 'intervals[i].length == 2', '0 ≤ starti ≤ endi ≤ 10⁴']
        }
    ]
    
    # Convert to proper format and add to problems
    for prob in arrays:
        prob['examples'] = json.dumps(prob['examples'])
        prob['hints'] = json.dumps(prob['hints'])
        prob['constraints'] = json.dumps(prob['constraints'])
        prob['tags'] = json.dumps(['Array'])
        problems.append(prob)
    
    return problems

if __name__ == "__main__":
    problems = create_all_problems()
    print(f"Generated {len(problems)} problems")
    for p in problems:
        print(f"- {p['title']} ({p['difficulty']}) - {p['topic']}")
