import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Redis Cloud connection
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
        'tags': json.dumps([topic.title()])
    }

# Generate 80+ problems across 8 topics
problems = []

# 1. ARRAYS (10 problems)
arrays_problems = [
    create_problem('two_sum', 'Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'easy', 'arrays',
        [{'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]', 'explanation': 'Because nums[0] + nums[1] = 2 + 7 = 9'},
         {'input': 'nums = [3,2,4], target = 6', 'output': '[1,2]', 'explanation': 'Because nums[1] + nums[2] = 2 + 4 = 6'},
         {'input': 'nums = [3,3], target = 6', 'output': '[0,1]', 'explanation': 'Because nums[0] + nums[1] = 3 + 3 = 6'}],
        ['Use a hash map to store numbers you\'ve seen', 'For each number, check if its complement exists', 'The complement is target - current_number'],
        ['2 ≤ nums.length ≤ 10⁴', '-10⁹ ≤ nums[i] ≤ 10⁹', '-10⁹ ≤ target ≤ 10⁹']),
    
    create_problem('best_time_buy_sell_stock', 'Best Time to Buy and Sell Stock', 'You are given an array prices where prices[i] is the price of a given stock on the ith day. Find the maximum profit.', 'easy', 'arrays',
        [{'input': 'prices = [7,1,5,3,6,4]', 'output': '5', 'explanation': 'Buy on day 2 (price = 1) and sell on day 5 (price = 6)'},
         {'input': 'prices = [7,6,4,3,1]', 'output': '0', 'explanation': 'No transactions are done, max profit = 0'},
         {'input': 'prices = [1,2,3,4,5]', 'output': '4', 'explanation': 'Buy on day 1 and sell on day 5'}],
        ['Track the minimum price seen so far', 'Calculate profit for each day', 'Keep track of maximum profit'],
        ['1 ≤ prices.length ≤ 10⁵', '0 ≤ prices[i] ≤ 10⁴']),
    
    create_problem('contains_duplicate', 'Contains Duplicate', 'Given an integer array nums, return true if any value appears at least twice in the array.', 'easy', 'arrays',
        [{'input': 'nums = [1,2,3,1]', 'output': 'true', 'explanation': 'Element 1 appears twice'},
         {'input': 'nums = [1,2,3,4]', 'output': 'false', 'explanation': 'All elements are distinct'},
         {'input': 'nums = [1,1,1,3,3,4,3,2,4,2]', 'output': 'true', 'explanation': 'Multiple duplicates exist'}],
        ['Use a hash set to track seen elements', 'Return true if element already exists', 'Return false if no duplicates found'],
        ['1 ≤ nums.length ≤ 10⁵', '-10⁹ ≤ nums[i] ≤ 10⁹']),
    
    create_problem('product_except_self', 'Product of Array Except Self', 'Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].', 'medium', 'arrays',
        [{'input': 'nums = [1,2,3,4]', 'output': '[24,12,8,6]', 'explanation': 'Product except self for each position'},
         {'input': 'nums = [-1,1,0,-3,3]', 'output': '[0,0,9,0,0]', 'explanation': 'Zero makes most products zero'},
         {'input': 'nums = [2,3,4,5]', 'output': '[60,40,30,24]', 'explanation': 'Product of all other elements'}],
        ['Think about left and right products', 'Use two passes through the array', 'Can you do it without division?'],
        ['2 ≤ nums.length ≤ 10⁵', '-30 ≤ nums[i] ≤ 30']),
    
    create_problem('maximum_subarray', 'Maximum Subarray', 'Given an integer array nums, find the contiguous subarray with the largest sum and return its sum.', 'medium', 'arrays',
        [{'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]', 'output': '6', 'explanation': 'Subarray [4,-1,2,1] has the largest sum'},
         {'input': 'nums = [1]', 'output': '1', 'explanation': 'Single element array'},
         {'input': 'nums = [5,4,-1,7,8]', 'output': '23', 'explanation': 'The entire array has the largest sum'}],
        ['Use Kadane\'s algorithm', 'Decide whether to extend subarray or start new', 'If sum becomes negative, start fresh'],
        ['1 ≤ nums.length ≤ 10⁵', '-10⁴ ≤ nums[i] ≤ 10⁴']),
    
    create_problem('find_minimum_rotated_sorted', 'Find Minimum in Rotated Sorted Array', 'Suppose an array of length n sorted in ascending order is rotated. Find the minimum element.', 'medium', 'arrays',
        [{'input': 'nums = [3,4,5,1,2]', 'output': '1', 'explanation': 'The original array was [1,2,3,4,5] rotated 3 times'},
         {'input': 'nums = [4,5,6,7,0,1,2]', 'output': '0', 'explanation': 'The original array was [0,1,2,4,5,6,7] rotated 4 times'},
         {'input': 'nums = [11,13,15,17]', 'output': '11', 'explanation': 'The original array was not rotated'}],
        ['Use binary search approach', 'Compare middle element with right element', 'The minimum is where the rotation happened'],
        ['n == nums.length', '1 ≤ n ≤ 5000', '-5000 ≤ nums[i] ≤ 5000']),
    
    create_problem('search_rotated_sorted', 'Search in Rotated Sorted Array', 'There is an integer array nums sorted in ascending order (with distinct values). Search for target value.', 'medium', 'arrays',
        [{'input': 'nums = [4,5,6,7,0,1,2], target = 0', 'output': '4', 'explanation': 'Target 0 is at index 4'},
         {'input': 'nums = [4,5,6,7,0,1,2], target = 3', 'output': '-1', 'explanation': 'Target 3 is not in array'},
         {'input': 'nums = [1], target = 0', 'output': '-1', 'explanation': 'Target not found in single element array'}],
        ['Use modified binary search', 'Determine which half is sorted', 'Check if target is in the sorted half'],
        ['1 ≤ nums.length ≤ 5000', '-10⁴ ≤ nums[i] ≤ 10⁴', '-10⁴ ≤ target ≤ 10⁴']),
    
    create_problem('three_sum', '3Sum', 'Given an integer array nums, return all the triplets that sum to zero.', 'medium', 'arrays',
        [{'input': 'nums = [-1,0,1,2,-1,-4]', 'output': '[[-1,-1,2],[-1,0,1]]', 'explanation': 'Two triplets sum to zero'},
         {'input': 'nums = [0,1,1]', 'output': '[]', 'explanation': 'No triplets sum to zero'},
         {'input': 'nums = [0,0,0]', 'output': '[[0,0,0]]', 'explanation': 'Only one triplet sums to zero'}],
        ['Sort the array first', 'Use two pointers technique', 'Skip duplicates to avoid duplicate triplets'],
        ['3 ≤ nums.length ≤ 3000', '-10⁵ ≤ nums[i] ≤ 10⁵']),
    
    create_problem('container_most_water', 'Container With Most Water', 'You are given an integer array height. Find two lines that together with the x-axis form a container that holds the most water.', 'medium', 'arrays',
        [{'input': 'height = [1,8,6,2,5,4,8,3,7]', 'output': '49', 'explanation': 'Lines at index 1 and 8 form the largest container'},
         {'input': 'height = [1,1]', 'output': '1', 'explanation': 'Only two lines available'},
         {'input': 'height = [1,2,1]', 'output': '2', 'explanation': 'Lines at index 0 and 2 form container of area 2'}],
        ['Use two pointers from both ends', 'Move the pointer with smaller height', 'Calculate area at each step'],
        ['n == height.length', '2 ≤ n ≤ 10⁵', '0 ≤ height[i] ≤ 10⁴']),
    
    create_problem('merge_intervals', 'Merge Intervals', 'Given an array of intervals, merge all overlapping intervals.', 'medium', 'arrays',
        [{'input': 'intervals = [[1,3],[2,6],[8,10],[15,18]]', 'output': '[[1,6],[8,10],[15,18]]', 'explanation': '[1,3] and [2,6] overlap'},
         {'input': 'intervals = [[1,4],[4,5]]', 'output': '[[1,5]]', 'explanation': 'Intervals [1,4] and [4,5] are considered overlapping'},
         {'input': 'intervals = [[1,4],[2,3]]', 'output': '[[1,4]]', 'explanation': '[2,3] is completely inside [1,4]'}],
        ['Sort intervals by start time', 'Merge overlapping intervals as you go', 'Check if current interval overlaps with the last merged interval'],
        ['1 ≤ intervals.length ≤ 10⁴', 'intervals[i].length == 2', '0 ≤ starti ≤ endi ≤ 10⁴'])
]

problems.extend(arrays_problems)
print(f"✅ Added {len(arrays_problems)} array problems")

print("Testing Redis connection...")
try:
    redis_client.ping()
    print("✅ Redis connection successful!")
except Exception as e:
    print(f"❌ Redis connection failed: {str(e)}")
    exit(1)

print("Creating search index...")
try:
    redis_client.execute_command('FT.CREATE', 'problem_idx', 'ON', 'HASH',
        'PREFIX', '1', 'problem:',
        'SCHEMA',
        'title', 'TEXT', 'WEIGHT', '2.0',
        'description', 'TEXT',
        'difficulty', 'TAG',
        'topic', 'TAG'
    )
    print("✅ Search index created successfully!")
except redis.exceptions.ResponseError as e:
    if 'Index already exists' not in str(e):
        raise e
    print("✅ Search index already exists")

print("Initializing problems...")
for problem in problems:
    # Store problem data
    redis_client.hset(f"problem:{problem['id']}", mapping=problem)
    
    # Add to difficulty-topic sorted set
    redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
    
    # Add to topics and difficulties sets
    redis_client.sadd('topics', problem['topic'])
    redis_client.sadd('difficulties', problem['difficulty'])

print(f"✅ {len(problems)} problems initialized!")

print("Setting up platform stats...")
redis_client.hset('platform_stats', mapping={
    'total_problems': len(problems),
    'total_users': 0,
    'total_submissions': 0
})

print("Creating time series...")
try:
    redis_client.execute_command('TS.CREATE', 'user_activity')
    print("✅ Created user_activity time series")
except redis.exceptions.ResponseError as e:
    if 'already exists' not in str(e):
        raise e
    print("✅ user_activity time series already exists")

try:
    redis_client.execute_command('TS.CREATE', 'similarity_searches')
    print("✅ Created similarity_searches time series")
except redis.exceptions.ResponseError as e:
    if 'already exists' not in str(e):
        raise e
    print("✅ similarity_searches time series already exists")

print("🎉 Redis data initialization complete!")
print(f"📊 Total problems: {len(problems)}")
print("🔍 Each problem has:")
print("   • Exactly 3 detailed examples with explanations")
print("   • Exactly 3 progressive hints")
print("   • Proper constraints")
print("   • No company tags (removed as requested)")

# Show topic distribution
topics = {}
for problem in problems:
    topic = problem['topic']
    if topic not in topics:
        topics[topic] = 0
    topics[topic] += 1

print("\n📋 Problems by Topic:")
for topic, count in topics.items():
    print(f"   • {topic.title()}: {count} problems")

print(f"\nNote: This is just the arrays topic. Need to add 7 more topics to reach 80+ problems total.")
