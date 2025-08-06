#!/usr/bin/env python3
"""
Create exactly 24 unique DSA problems
8 topics × 3 difficulties = 24 unique problems
No duplicates, one problem per topic per difficulty
"""

import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_redis_client():
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        password=os.getenv('REDIS_PASSWORD', ''),
        decode_responses=True
    )

# Exactly 24 unique problems - 8 topics × 3 difficulties
UNIQUE_24_PROBLEMS = {
    # ARRAYS (3 problems)
    "two_sum": {
        "id": "two_sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "topic": "arrays",
        "category": "Arrays",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."}],
        "constraints": ["2 ≤ nums.length ≤ 10⁴", "-10⁹ ≤ nums[i] ≤ 10⁹", "-10⁹ ≤ target ≤ 10⁹", "Only one valid answer exists."],
        "leetcode_url": "https://leetcode.com/problems/two-sum/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n) with hash map approach",
        "space_complexity": "O(n) for hash map storage",
        "hints": ["Use a hash map to store numbers and their indices", "For each number, check if its complement exists in the hash map"],
        "solution_template": "def twoSum(self, nums: List[int], target: int) -> List[int]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]}]
    },
    
    "three_sum": {
        "id": "three_sum",
        "title": "3Sum",
        "difficulty": "medium",
        "topic": "arrays",
        "category": "Arrays",
        "description": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.",
        "examples": [{"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]", "explanation": "The distinct triplets are [-1,0,1] and [-1,-1,2]."}],
        "constraints": ["3 ≤ nums.length ≤ 3000", "-10⁵ ≤ nums[i] ≤ 10⁵"],
        "leetcode_url": "https://leetcode.com/problems/3sum/",
        "companies": ["Amazon", "Microsoft", "Facebook", "Google", "Adobe"],
        "time_complexity": "O(n²) with two pointers",
        "space_complexity": "O(1) excluding output array",
        "hints": ["Sort the array first", "Use two pointers technique", "Skip duplicates carefully"],
        "solution_template": "def threeSum(self, nums: List[int]) -> List[List[int]]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "expected": [[-1, -1, 2], [-1, 0, 1]]}]
    },
    
    "four_sum": {
        "id": "four_sum",
        "title": "4Sum",
        "difficulty": "hard",
        "topic": "arrays",
        "category": "Arrays",
        "description": "Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that nums[a] + nums[b] + nums[c] + nums[d] == target.",
        "examples": [{"input": "nums = [1,0,-1,0,-2,2], target = 0", "output": "[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]", "explanation": "The distinct quadruplets sum to target."}],
        "constraints": ["1 ≤ nums.length ≤ 200", "-10⁹ ≤ nums[i] ≤ 10⁹", "-10⁹ ≤ target ≤ 10⁹"],
        "leetcode_url": "https://leetcode.com/problems/4sum/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook"],
        "time_complexity": "O(n³) with optimizations",
        "space_complexity": "O(1) excluding output array",
        "hints": ["Use nested loops with two pointers", "Skip duplicates carefully", "Optimize with early termination"],
        "solution_template": "def fourSum(self, nums: List[int], target: int) -> List[List[int]]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"nums": [1, 0, -1, 0, -2, 2], "target": 0}, "expected": [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]}]
    },

    # STRINGS (3 problems)
    "valid_palindrome": {
        "id": "valid_palindrome",
        "title": "Valid Palindrome",
        "difficulty": "easy",
        "topic": "strings",
        "category": "Strings",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
        "examples": [{"input": 's = "A man, a plan, a canal: Panama"', "output": "true", "explanation": '"amanaplanacanalpanama" is a palindrome.'}],
        "constraints": ["1 ≤ s.length ≤ 2 × 10⁵", "s consists only of printable ASCII characters."],
        "leetcode_url": "https://leetcode.com/problems/valid-palindrome/",
        "companies": ["Microsoft", "Amazon", "Facebook", "Google", "Apple"],
        "time_complexity": "O(n) where n is length of string",
        "space_complexity": "O(1) with two pointers",
        "hints": ["Use two pointers technique", "Skip non-alphanumeric characters"],
        "solution_template": "def isPalindrome(self, s: str) -> bool:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True}]
    },
    
    "longest_palindromic_substring": {
        "id": "longest_palindromic_substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "medium",
        "topic": "strings",
        "category": "Strings",
        "description": "Given a string s, return the longest palindromic substring in s.",
        "examples": [{"input": 's = "babad"', "output": '"bab"', "explanation": '"aba" is also a valid answer.'}],
        "constraints": ["1 ≤ s.length ≤ 1000", "s consist of only digits and English letters."],
        "leetcode_url": "https://leetcode.com/problems/longest-palindromic-substring/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n²) with expand around centers",
        "space_complexity": "O(1) space complexity",
        "hints": ["Expand around centers", "Consider both odd and even length palindromes"],
        "solution_template": "def longestPalindrome(self, s: str) -> str:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"s": "babad"}, "expected": "bab"}]
    },
    
    "edit_distance": {
        "id": "edit_distance",
        "title": "Edit Distance",
        "difficulty": "hard",
        "topic": "strings",
        "category": "Strings",
        "description": "Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2. You have three operations: insert, delete, replace a character.",
        "examples": [{"input": 'word1 = "horse", word2 = "ros"', "output": "3", "explanation": "horse -> rorse (replace 'h' with 'r'), rorse -> rose (remove 'r'), rose -> ros (remove 'e')"}],
        "constraints": ["0 ≤ word1.length, word2.length ≤ 500", "word1 and word2 consist of lowercase English letters."],
        "leetcode_url": "https://leetcode.com/problems/edit-distance/",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(m × n) where m, n are string lengths",
        "space_complexity": "O(m × n) for DP table",
        "hints": ["Use dynamic programming", "dp[i][j] = min operations to convert word1[0:i] to word2[0:j]"],
        "solution_template": "def minDistance(self, word1: str, word2: str) -> int:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"word1": "horse", "word2": "ros"}, "expected": 3}]
    }
}

def clean_and_create_unique_problems():
    """Clean existing problems and create exactly 24 unique ones"""
    redis_client = get_redis_client()
    
    print("🧹 CLEANING EXISTING PROBLEMS...")
    
    # Delete all existing problems
    existing_keys = list(redis_client.scan_iter(match="problem:*"))
    if existing_keys:
        redis_client.delete(*existing_keys)
        print(f"🗑️ Deleted {len(existing_keys)} existing problems")
    
    # Clear all indices
    redis_client.delete("all_problems")
    for difficulty in ["easy", "medium", "hard"]:
        redis_client.delete(f"problems_by_difficulty:{difficulty}")
    
    topics = ["arrays", "strings", "trees", "linked_lists", "dynamic_programming", "graphs", "stacks", "hash_tables"]
    for topic in topics:
        redis_client.delete(f"problems_by_topic:{topic}")
    
    print("✅ Database cleaned")
    print()
    print("🚀 CREATING 24 UNIQUE PROBLEMS...")
    print("📊 Target: 8 topics × 3 difficulties = 24 unique problems")
    print()
    
    # Add the first 6 problems (Arrays + Strings)
    for problem_id, problem_data in UNIQUE_24_PROBLEMS.items():
        # Store problem data
        problem_key = f"problem:{problem_id}"
        
        # Convert lists to JSON strings for Redis storage
        problem_redis_data = {
            "id": problem_data["id"],
            "title": problem_data["title"],
            "difficulty": problem_data["difficulty"],
            "topic": problem_data["topic"],
            "category": problem_data["category"],
            "description": problem_data["description"],
            "examples": json.dumps(problem_data["examples"]),
            "constraints": json.dumps(problem_data["constraints"]),
            "leetcode_url": problem_data["leetcode_url"],
            "companies": json.dumps(problem_data["companies"]),
            "time_complexity": problem_data["time_complexity"],
            "space_complexity": problem_data["space_complexity"],
            "hints": json.dumps(problem_data["hints"]),
            "solution_template": problem_data["solution_template"],
            "test_cases": json.dumps(problem_data["test_cases"])
        }
        
        # Store in Redis
        redis_client.hset(problem_key, mapping=problem_redis_data)
        
        # Add to indices
        redis_client.sadd(f"problems_by_topic:{problem_data['topic']}", problem_id)
        redis_client.sadd(f"problems_by_difficulty:{problem_data['difficulty']}", problem_id)
        redis_client.sadd("all_problems", problem_id)
        
        print(f"✅ Added: {problem_data['title']} ({problem_data['difficulty']}) - {problem_data['topic']}")
    
    print(f"\n📊 PROGRESS: {len(UNIQUE_24_PROBLEMS)}/24 problems added")
    print("🔄 This script adds Arrays + Strings topics (6 problems)")
    print("📝 Need to create remaining 18 problems for other topics")
    
    return len(UNIQUE_24_PROBLEMS)

if __name__ == "__main__":
    count = clean_and_create_unique_problems()
    print(f"\n🎯 NEXT STEPS:")
    print("1. Run this script to clean database and add Arrays + Strings")
    print("2. Create similar scripts for remaining 6 topics")
    print("3. Ensure exactly 24 unique problems total")
    print(f"\n✅ Current: {count} problems added")
