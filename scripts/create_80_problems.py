#!/usr/bin/env python3
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
        'id': id, 'title': title, 'description': description,
        'difficulty': difficulty, 'topic': topic,
        'examples': json.dumps(examples),
        'hints': json.dumps(hints),
        'constraints': json.dumps(constraints),
        'tags': json.dumps([topic.title().replace('-', ' ')])
    }

# Generate 80+ problems across 8 topics (10+ each)
problems = []

# 1. ARRAYS (10 problems)
arrays = [
    ['two_sum', 'Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'easy'],
    ['best_time_buy_sell_stock', 'Best Time to Buy and Sell Stock', 'Find the maximum profit from buying and selling stock once.', 'easy'],
    ['contains_duplicate', 'Contains Duplicate', 'Return true if any value appears at least twice in the array.', 'easy'],
    ['product_except_self', 'Product of Array Except Self', 'Return array where each element is product of all other elements.', 'medium'],
    ['maximum_subarray', 'Maximum Subarray', 'Find the contiguous subarray with the largest sum.', 'medium'],
    ['find_minimum_rotated_sorted', 'Find Minimum in Rotated Sorted Array', 'Find minimum element in rotated sorted array.', 'medium'],
    ['search_rotated_sorted', 'Search in Rotated Sorted Array', 'Search for target in rotated sorted array.', 'medium'],
    ['three_sum', '3Sum', 'Find all unique triplets that sum to zero.', 'medium'],
    ['container_most_water', 'Container With Most Water', 'Find two lines that form container with most water.', 'medium'],
    ['merge_intervals', 'Merge Intervals', 'Merge all overlapping intervals.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(arrays):
    problems.append(create_problem(id, title, desc, diff, 'arrays',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 2. STRINGS (10 problems)
strings = [
    ['valid_anagram', 'Valid Anagram', 'Check if two strings are anagrams.', 'easy'],
    ['valid_palindrome', 'Valid Palindrome', 'Check if string is palindrome ignoring non-alphanumeric.', 'easy'],
    ['longest_substring_no_repeat', 'Longest Substring Without Repeating Characters', 'Find longest substring without repeating characters.', 'medium'],
    ['group_anagrams', 'Group Anagrams', 'Group strings that are anagrams together.', 'medium'],
    ['valid_parentheses', 'Valid Parentheses', 'Check if parentheses are valid.', 'easy'],
    ['longest_palindromic_substring', 'Longest Palindromic Substring', 'Find the longest palindromic substring.', 'medium'],
    ['palindromic_substrings', 'Palindromic Substrings', 'Count palindromic substrings.', 'medium'],
    ['encode_decode_strings', 'Encode and Decode Strings', 'Encode list of strings to string and decode back.', 'medium'],
    ['minimum_window_substring', 'Minimum Window Substring', 'Find minimum window substring containing all characters.', 'hard'],
    ['character_replacement', 'Longest Repeating Character Replacement', 'Longest substring with same letter after k replacements.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(strings):
    problems.append(create_problem(id, title, desc, diff, 'strings',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 3. LINKED LISTS (10 problems)
linked_lists = [
    ['reverse_linked_list', 'Reverse Linked List', 'Reverse a singly linked list.', 'easy'],
    ['merge_two_sorted_lists', 'Merge Two Sorted Lists', 'Merge two sorted linked lists.', 'easy'],
    ['linked_list_cycle', 'Linked List Cycle', 'Detect if linked list has a cycle.', 'easy'],
    ['remove_nth_from_end', 'Remove Nth Node From End of List', 'Remove nth node from end of list.', 'medium'],
    ['reorder_list', 'Reorder List', 'Reorder list in specific pattern.', 'medium'],
    ['merge_k_sorted_lists', 'Merge k Sorted Lists', 'Merge k sorted linked lists.', 'hard'],
    ['find_duplicate_number', 'Find the Duplicate Number', 'Find duplicate number in array using linked list cycle detection.', 'medium'],
    ['add_two_numbers', 'Add Two Numbers', 'Add two numbers represented as linked lists.', 'medium'],
    ['intersection_two_linked_lists', 'Intersection of Two Linked Lists', 'Find intersection point of two linked lists.', 'easy'],
    ['palindrome_linked_list', 'Palindrome Linked List', 'Check if linked list is palindrome.', 'easy']
]

for i, (id, title, desc, diff) in enumerate(linked_lists):
    problems.append(create_problem(id, title, desc, diff, 'linked-lists',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 4. TREES (10 problems)
trees = [
    ['maximum_depth_binary_tree', 'Maximum Depth of Binary Tree', 'Find maximum depth of binary tree.', 'easy'],
    ['same_tree', 'Same Tree', 'Check if two binary trees are the same.', 'easy'],
    ['invert_binary_tree', 'Invert Binary Tree', 'Invert a binary tree.', 'easy'],
    ['binary_tree_maximum_path_sum', 'Binary Tree Maximum Path Sum', 'Find maximum path sum in binary tree.', 'hard'],
    ['binary_tree_level_order_traversal', 'Binary Tree Level Order Traversal', 'Return level order traversal of binary tree.', 'medium'],
    ['serialize_deserialize_binary_tree', 'Serialize and Deserialize Binary Tree', 'Serialize and deserialize binary tree.', 'hard'],
    ['subtree_of_another_tree', 'Subtree of Another Tree', 'Check if tree is subtree of another.', 'easy'],
    ['construct_binary_tree_preorder_inorder', 'Construct Binary Tree from Preorder and Inorder', 'Construct tree from preorder and inorder traversal.', 'medium'],
    ['validate_binary_search_tree', 'Validate Binary Search Tree', 'Check if tree is valid BST.', 'medium'],
    ['kth_smallest_element_bst', 'Kth Smallest Element in BST', 'Find kth smallest element in BST.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(trees):
    problems.append(create_problem(id, title, desc, diff, 'trees',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 5. GRAPHS (10 problems)
graphs = [
    ['number_of_islands', 'Number of Islands', 'Count number of islands in 2D grid.', 'medium'],
    ['clone_graph', 'Clone Graph', 'Clone an undirected graph.', 'medium'],
    ['pacific_atlantic_water_flow', 'Pacific Atlantic Water Flow', 'Find cells where water can flow to both oceans.', 'medium'],
    ['course_schedule', 'Course Schedule', 'Check if all courses can be finished.', 'medium'],
    ['course_schedule_ii', 'Course Schedule II', 'Return order of courses to finish all.', 'medium'],
    ['graph_valid_tree', 'Graph Valid Tree', 'Check if graph forms a valid tree.', 'medium'],
    ['number_connected_components', 'Number of Connected Components in Undirected Graph', 'Count connected components.', 'medium'],
    ['alien_dictionary', 'Alien Dictionary', 'Find order of characters in alien language.', 'hard'],
    ['word_ladder', 'Word Ladder', 'Find shortest transformation sequence.', 'hard'],
    ['redundant_connection', 'Redundant Connection', 'Find redundant edge in graph.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(graphs):
    problems.append(create_problem(id, title, desc, diff, 'graphs',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 6. DYNAMIC PROGRAMMING (10 problems)
dp = [
    ['climbing_stairs', 'Climbing Stairs', 'Count ways to climb stairs.', 'easy'],
    ['coin_change', 'Coin Change', 'Find minimum coins to make amount.', 'medium'],
    ['longest_increasing_subsequence', 'Longest Increasing Subsequence', 'Find length of longest increasing subsequence.', 'medium'],
    ['longest_common_subsequence', 'Longest Common Subsequence', 'Find length of longest common subsequence.', 'medium'],
    ['word_break', 'Word Break', 'Check if string can be segmented into dictionary words.', 'medium'],
    ['combination_sum_iv', 'Combination Sum IV', 'Count combinations that add up to target.', 'medium'],
    ['house_robber', 'House Robber', 'Maximum money that can be robbed.', 'medium'],
    ['house_robber_ii', 'House Robber II', 'House robber with circular arrangement.', 'medium'],
    ['decode_ways', 'Decode Ways', 'Count ways to decode string.', 'medium'],
    ['unique_paths', 'Unique Paths', 'Count unique paths in grid.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(dp):
    problems.append(create_problem(id, title, desc, diff, 'dynamic-programming',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 7. STACKS (10 problems)
stacks = [
    ['valid_parentheses_stack', 'Valid Parentheses', 'Check if parentheses are valid using stack.', 'easy'],
    ['min_stack', 'Min Stack', 'Design stack with min operation.', 'easy'],
    ['evaluate_reverse_polish_notation', 'Evaluate Reverse Polish Notation', 'Evaluate RPN expression.', 'medium'],
    ['generate_parentheses', 'Generate Parentheses', 'Generate all valid parentheses combinations.', 'medium'],
    ['daily_temperatures', 'Daily Temperatures', 'Find next warmer temperature.', 'medium'],
    ['car_fleet', 'Car Fleet', 'Count car fleets reaching destination.', 'medium'],
    ['largest_rectangle_histogram', 'Largest Rectangle in Histogram', 'Find largest rectangle in histogram.', 'hard'],
    ['trapping_rain_water', 'Trapping Rain Water', 'Calculate trapped rain water.', 'hard'],
    ['next_greater_element', 'Next Greater Element I', 'Find next greater element.', 'easy'],
    ['asteroid_collision', 'Asteroid Collision', 'Simulate asteroid collision.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(stacks):
    problems.append(create_problem(id, title, desc, diff, 'stacks',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

# 8. HEAPS (10 problems)
heaps = [
    ['kth_largest_element', 'Kth Largest Element in Array', 'Find kth largest element.', 'medium'],
    ['top_k_frequent_elements', 'Top K Frequent Elements', 'Find k most frequent elements.', 'medium'],
    ['find_median_data_stream', 'Find Median from Data Stream', 'Find median from data stream.', 'hard'],
    ['merge_k_sorted_lists_heap', 'Merge k Sorted Lists', 'Merge k sorted lists using heap.', 'hard'],
    ['task_scheduler', 'Task Scheduler', 'Schedule tasks with cooling time.', 'medium'],
    ['design_twitter', 'Design Twitter', 'Design simplified Twitter.', 'medium'],
    ['ugly_number_ii', 'Ugly Number II', 'Find nth ugly number.', 'medium'],
    ['sliding_window_maximum', 'Sliding Window Maximum', 'Find maximum in sliding window.', 'hard'],
    ['meeting_rooms_ii', 'Meeting Rooms II', 'Find minimum meeting rooms needed.', 'medium'],
    ['reorganize_string', 'Reorganize String', 'Reorganize string so no adjacent chars are same.', 'medium']
]

for i, (id, title, desc, diff) in enumerate(heaps):
    problems.append(create_problem(id, title, desc, diff, 'heaps',
        [{'input': f'Example {j+1} input', 'output': f'Output {j+1}', 'explanation': f'Explanation {j+1}'} for j in range(3)],
        [f'Hint {j+1} for {title}' for j in range(3)],
        [f'Constraint {j+1}' for j in range(3)]))

print(f"Generated {len(problems)} problems across 8 topics!")

# Initialize Redis
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
    print("✅ Search index created!")
except redis.exceptions.ResponseError as e:
    if 'Index already exists' not in str(e):
        raise e
    print("✅ Search index already exists")

print("Initializing problems...")
for problem in problems:
    redis_client.hset(f"problem:{problem['id']}", mapping=problem)
    redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
    redis_client.sadd('topics', problem['topic'])
    redis_client.sadd('difficulties', problem['difficulty'])

print(f"✅ {len(problems)} problems initialized!")

# Show distribution
topics = {}
for problem in problems:
    topic = problem['topic']
    topics[topic] = topics.get(topic, 0) + 1

print("\n📋 Problems by Topic:")
for topic, count in sorted(topics.items()):
    print(f"   • {topic.title().replace('-', ' ')}: {count} problems")

print(f"\n🎉 Total: {len(problems)} problems across {len(topics)} topics!")
