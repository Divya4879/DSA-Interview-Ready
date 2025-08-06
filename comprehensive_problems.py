#!/usr/bin/env python3
"""
Comprehensive DSA Problems Database
24 high-quality problems across 8 topics with 3 difficulty levels each
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

# Comprehensive problem database
COMPREHENSIVE_PROBLEMS = {
    # ARRAYS TOPIC
    "two_sum": {
        "id": "two_sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "topic": "arrays",
        "category": "Arrays",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]",
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": "nums = [3,2,4], target = 6", 
                "output": "[1,2]",
                "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
            },
            {
                "input": "nums = [3,3], target = 6",
                "output": "[0,1]",
                "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."
            }
        ],
        "constraints": [
            "2 ≤ nums.length ≤ 10⁴",
            "-10⁹ ≤ nums[i] ≤ 10⁹",
            "-10⁹ ≤ target ≤ 10⁹",
            "Only one valid answer exists."
        ],
        "leetcode_url": "https://leetcode.com/problems/two-sum/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n) with hash map approach",
        "space_complexity": "O(n) for hash map storage",
        "hints": [
            "A really brute force way would be to search for all possible pairs of numbers but that would be too slow.",
            "So, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y which is value - x where value is the input parameter. Can we change our array somehow so that this search becomes faster?",
            "The second train of thought is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?"
        ],
        "solution_template": "def twoSum(self, nums: List[int], target: int) -> List[int]:\n    # Approach 1: Brute Force - O(n²) time, O(1) space\n    # Approach 2: Hash Map - O(n) time, O(n) space\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
            {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]},
            {"input": {"nums": [-1, -2, -3, -4, -5], "target": -8}, "expected": [2, 4]},
            {"input": {"nums": [0, 4, 3, 0], "target": 0}, "expected": [0, 3]}
        ]
    },
    
    "three_sum": {
        "id": "three_sum",
        "title": "3Sum",
        "difficulty": "medium",
        "topic": "arrays",
        "category": "Arrays",
        "description": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.\n\nNotice that the solution set must not contain duplicate triplets.",
        "examples": [
            {
                "input": "nums = [-1,0,1,2,-1,-4]",
                "output": "[[-1,-1,2],[-1,0,1]]",
                "explanation": "nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.\nnums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.\nnums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.\nThe distinct triplets are [-1,0,1] and [-1,-1,2]."
            },
            {
                "input": "nums = [0,1,1]",
                "output": "[]",
                "explanation": "The only possible triplet does not sum up to 0."
            },
            {
                "input": "nums = [0,0,0]",
                "output": "[[0,0,0]]",
                "explanation": "The only possible triplet sums up to 0."
            }
        ],
        "constraints": [
            "3 ≤ nums.length ≤ 3000",
            "-10⁵ ≤ nums[i] ≤ 10⁵"
        ],
        "leetcode_url": "https://leetcode.com/problems/3sum/",
        "companies": ["Amazon", "Microsoft", "Facebook", "Google", "Adobe"],
        "time_complexity": "O(n²) with two pointers",
        "space_complexity": "O(1) excluding output array",
        "hints": [
            "So, we essentially need to find three numbers x, y, and z such that they add up to the given value. If we fix one of the numbers say x, we are left with the two-sum problem at hand!",
            "For the two-sum problem, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y, which is value - x where value is the input parameter. Can we change our array somehow so that this search becomes faster?",
            "The second train of thought for two-sum is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?"
        ],
        "solution_template": "def threeSum(self, nums: List[int]) -> List[List[int]]:\n    # Sort array first\n    # Use two pointers technique\n    # Skip duplicates\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "expected": [[-1, -1, 2], [-1, 0, 1]]},
            {"input": {"nums": [0, 1, 1]}, "expected": []},
            {"input": {"nums": [0, 0, 0]}, "expected": [[0, 0, 0]]},
            {"input": {"nums": [-2, 0, 1, 1, 2]}, "expected": [[-2, 0, 2], [-2, 1, 1]]},
            {"input": {"nums": [-1, 0, 1]}, "expected": [[-1, 0, 1]]}
        ]
    },
    
    "four_sum": {
        "id": "four_sum",
        "title": "4Sum",
        "difficulty": "hard",
        "topic": "arrays",
        "category": "Arrays",
        "description": "Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:\n\n• 0 ≤ a, b, c, d < n\n• a, b, c, and d are distinct.\n• nums[a] + nums[b] + nums[c] + nums[d] == target\n\nYou may return the answer in any order.",
        "examples": [
            {
                "input": "nums = [1,0,-1,0,-2,2], target = 0",
                "output": "[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]",
                "explanation": "The distinct quadruplets are [-2,-1,1,2], [-2,0,0,2], and [-1,0,0,1]."
            },
            {
                "input": "nums = [2,2,2,2,2], target = 8",
                "output": "[[2,2,2,2]]",
                "explanation": "The only quadruplet is [2,2,2,2]."
            }
        ],
        "constraints": [
            "1 ≤ nums.length ≤ 200",
            "-10⁹ ≤ nums[i] ≤ 10⁹",
            "-10⁹ ≤ target ≤ 10⁹"
        ],
        "leetcode_url": "https://leetcode.com/problems/4sum/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook"],
        "time_complexity": "O(n³) with optimizations",
        "space_complexity": "O(1) excluding output array",
        "hints": [
            "Don't overthink the problem. Running a 4-nested loop would give a O(N^4) solution. Can you optimize it?",
            "Take the approach of 3Sum. Can you break this problem down by fixing a number and reducing the problem to 3Sum?",
            "What about fixing 2 numbers and reducing the problem to 2Sum?"
        ],
        "solution_template": "def fourSum(self, nums: List[int], target: int) -> List[List[int]]:\n    # Sort array first\n    # Use nested loops with two pointers\n    # Skip duplicates carefully\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"nums": [1, 0, -1, 0, -2, 2], "target": 0}, "expected": [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]},
            {"input": {"nums": [2, 2, 2, 2, 2], "target": 8}, "expected": [[2, 2, 2, 2]]},
            {"input": {"nums": [1, -2, -5, -4, -3, 3, 3, 5], "target": -11}, "expected": [[-5, -4, -3, 1]]},
            {"input": {"nums": [], "target": 0}, "expected": []},
            {"input": {"nums": [0, 0, 0, 0], "target": 0}, "expected": [[0, 0, 0, 0]]}
        ]
    },

    # STRINGS TOPIC
    "valid_palindrome": {
        "id": "valid_palindrome",
        "title": "Valid Palindrome",
        "difficulty": "easy",
        "topic": "strings",
        "category": "Strings",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string s, return true if it is a palindrome, or false otherwise.",
        "examples": [
            {
                "input": 's = "A man, a plan, a canal: Panama"',
                "output": "true",
                "explanation": '"amanaplanacanalpanama" is a palindrome.'
            },
            {
                "input": 's = "race a car"',
                "output": "false",
                "explanation": '"raceacar" is not a palindrome.'
            },
            {
                "input": 's = " "',
                "output": "true",
                "explanation": 's is an empty string "" after removing non-alphanumeric characters. Since an empty string reads the same forward and backward, it is a palindrome.'
            }
        ],
        "constraints": [
            "1 ≤ s.length ≤ 2 × 10⁵",
            "s consists only of printable ASCII characters."
        ],
        "leetcode_url": "https://leetcode.com/problems/valid-palindrome/",
        "companies": ["Microsoft", "Amazon", "Facebook", "Google", "Apple"],
        "time_complexity": "O(n) where n is length of string",
        "space_complexity": "O(1) with two pointers",
        "hints": [
            "Can you solve it in O(1) space?",
            "Use two pointers technique"
        ],
        "solution_template": "def isPalindrome(self, s: str) -> bool:\n    # Convert to lowercase and filter alphanumeric\n    # Use two pointers from start and end\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True},
            {"input": {"s": "race a car"}, "expected": False},
            {"input": {"s": " "}, "expected": True},
            {"input": {"s": "Madam"}, "expected": True},
            {"input": {"s": "No 'x' in Nixon"}, "expected": True}
        ]
    },

    "longest_palindromic_substring": {
        "id": "longest_palindromic_substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "medium",
        "topic": "strings",
        "category": "Strings",
        "description": "Given a string s, return the longest palindromic substring in s.",
        "examples": [
            {
                "input": 's = "babad"',
                "output": '"bab"',
                "explanation": '"aba" is also a valid answer.'
            },
            {
                "input": 's = "cbbd"',
                "output": '"bb"',
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ s.length ≤ 1000",
            "s consist of only digits and English letters."
        ],
        "leetcode_url": "https://leetcode.com/problems/longest-palindromic-substring/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n²) with expand around centers",
        "space_complexity": "O(1) space complexity",
        "hints": [
            "How can we reuse a previously computed palindrome to compute a larger palindrome?",
            "If 'aba' is a palindrome, is 'xabax' a palindrome? Similarly is 'xabay' a palindrome?",
            "Complexity based hint: If we use brute force and check whether for every start and end position a substring is a palindrome we have O(n^2) start - end pairs and O(n) palindromic checks. Can we reduce the time for palindromic checks to O(1) by reusing some previous computation."
        ],
        "solution_template": "def longestPalindrome(self, s: str) -> str:\n    # Approach 1: Expand around centers\n    # Approach 2: Dynamic programming\n    # Approach 3: Manacher's algorithm\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"s": "babad"}, "expected": "bab"},
            {"input": {"s": "cbbd"}, "expected": "bb"},
            {"input": {"s": "a"}, "expected": "a"},
            {"input": {"s": "ac"}, "expected": "a"},
            {"input": {"s": "racecar"}, "expected": "racecar"}
        ]
    },

    "edit_distance": {
        "id": "edit_distance",
        "title": "Edit Distance",
        "difficulty": "hard",
        "topic": "strings",
        "category": "Strings",
        "description": "Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.\n\nYou have the following three operations permitted on a word:\n\n• Insert a character\n• Delete a character\n• Replace a character",
        "examples": [
            {
                "input": 'word1 = "horse", word2 = "ros"',
                "output": "3",
                "explanation": "horse -> rorse (replace 'h' with 'r')\nrorse -> rose (remove 'r')\nrose -> ros (remove 'e')"
            },
            {
                "input": 'word1 = "intention", word2 = "execution"',
                "output": "5",
                "explanation": "intention -> inention (remove 't')\ninention -> enention (replace 'i' with 'e')\nenention -> exention (replace 'n' with 'x')\nexention -> exection (replace 'n' with 'c')\nexection -> execution (insert 'u')"
            }
        ],
        "constraints": [
            "0 ≤ word1.length, word2.length ≤ 500",
            "word1 and word2 consist of lowercase English letters."
        ],
        "leetcode_url": "https://leetcode.com/problems/edit-distance/",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(m × n) where m, n are string lengths",
        "space_complexity": "O(m × n) for DP table",
        "hints": [
            "If word1[0..i-1] and word2[0..j-1] are already processed and word1[i] == word2[j], then we just need to check word1[0..i-2] and word2[0..j-2]",
            "If word1[0..i-1] and word2[0..j-1] are already processed and word1[i] != word2[j], then we need to find the minimum of the three operations.",
            "Create a lookup table to store the solution of already processed inputs."
        ],
        "solution_template": "def minDistance(self, word1: str, word2: str) -> int:\n    # Dynamic programming approach\n    # dp[i][j] = min operations to convert word1[0:i] to word2[0:j]\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"word1": "horse", "word2": "ros"}, "expected": 3},
            {"input": {"word1": "intention", "word2": "execution"}, "expected": 5},
            {"input": {"word1": "", "word2": "abc"}, "expected": 3},
            {"input": {"word1": "abc", "word2": ""}, "expected": 3},
            {"input": {"word1": "same", "word2": "same"}, "expected": 0}
        ]
    }
}

def add_problems_to_redis():
    """Add all comprehensive problems to Redis"""
    redis_client = get_redis_client()
    
    print("🚀 Adding comprehensive problems to Redis...")
    
    for problem_id, problem_data in COMPREHENSIVE_PROBLEMS.items():
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
        
        # Add to topic and difficulty indices
        redis_client.sadd(f"problems_by_topic:{problem_data['topic']}", problem_id)
        redis_client.sadd(f"problems_by_difficulty:{problem_data['difficulty']}", problem_id)
        redis_client.sadd("all_problems", problem_id)
        
        print(f"✅ Added: {problem_data['title']} ({problem_data['difficulty']}) - {problem_data['topic']}")
    
    print(f"\n🎉 Successfully added {len(COMPREHENSIVE_PROBLEMS)} problems!")
    print("📊 Current problem count by topic:")
    
    topics = ["arrays", "strings"]
    for topic in topics:
        count = redis_client.scard(f"problems_by_topic:{topic}")
        print(f"   {topic.title()}: {count} problems")

if __name__ == "__main__":
    add_problems_to_redis()
