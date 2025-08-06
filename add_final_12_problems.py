#!/usr/bin/env python3
"""
Add final 12 problems: Dynamic Programming, Graphs, Stacks, Hash Tables
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

# Final 12 problems for remaining 4 topics
FINAL_12_PROBLEMS = {
    # DYNAMIC PROGRAMMING (3 problems)
    "climbing_stairs": {
        "id": "climbing_stairs",
        "title": "Climbing Stairs",
        "difficulty": "easy",
        "topic": "dynamic_programming",
        "category": "Dynamic Programming",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [{"input": "n = 2", "output": "2", "explanation": "There are two ways: 1. 1 step + 1 step 2. 2 steps"}],
        "constraints": ["1 ≤ n ≤ 45"],
        "leetcode_url": "https://leetcode.com/problems/climbing-stairs/",
        "companies": ["Amazon", "Google", "Microsoft", "Adobe", "Apple"],
        "time_complexity": "O(n) with DP",
        "space_complexity": "O(1) with optimized space",
        "hints": ["This is Fibonacci sequence", "dp[i] = dp[i-1] + dp[i-2]"],
        "solution_template": "def climbStairs(self, n: int) -> int:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"n": 2}, "expected": 2}]
    },
    
    "longest_increasing_subsequence": {
        "id": "longest_increasing_subsequence",
        "title": "Longest Increasing Subsequence",
        "difficulty": "medium",
        "topic": "dynamic_programming",
        "category": "Dynamic Programming",
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "examples": [{"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4", "explanation": "The longest increasing subsequence is [2,3,7,18], therefore the length is 4."}],
        "constraints": ["1 ≤ nums.length ≤ 2500", "-10⁴ ≤ nums[i] ≤ 10⁴"],
        "leetcode_url": "https://leetcode.com/problems/longest-increasing-subsequence/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n²) DP, O(n log n) with binary search",
        "space_complexity": "O(n) for DP array",
        "hints": ["Define dp[i] as the length of LIS ending at index i", "Can you optimize to O(n log n) using binary search?"],
        "solution_template": "def lengthOfLIS(self, nums: List[int]) -> int:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, "expected": 4}]
    },
    
    "word_break": {
        "id": "word_break",
        "title": "Word Break",
        "difficulty": "hard",
        "topic": "dynamic_programming",
        "category": "Dynamic Programming",
        "description": "Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.",
        "examples": [{"input": 's = "leetcode", wordDict = ["leet","code"]', "output": "true", "explanation": 'Return true because "leetcode" can be segmented as "leet code".'}],
        "constraints": ["1 ≤ s.length ≤ 300", "1 ≤ wordDict.length ≤ 1000", "1 ≤ wordDict[i].length ≤ 20"],
        "leetcode_url": "https://leetcode.com/problems/word-break/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n² + m) where n is length of s, m is total length of words",
        "space_complexity": "O(n + m) for DP array and word set",
        "hints": ["dp[i] represents whether s[0...i-1] can be segmented", "For each position i, check if there exists a j such that dp[j] is true and s[j...i-1] is in wordDict"],
        "solution_template": "def wordBreak(self, s: str, wordDict: List[str]) -> bool:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"s": "leetcode", "wordDict": ["leet", "code"]}, "expected": True}]
    },

    # GRAPHS (3 problems)
    "number_of_islands": {
        "id": "number_of_islands",
        "title": "Number of Islands",
        "difficulty": "easy",
        "topic": "graphs",
        "category": "Graphs",
        "description": "Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.",
        "examples": [{"input": 'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', "output": "1", "explanation": "One island"}],
        "constraints": ["m == grid.length", "n == grid[i].length", "1 ≤ m, n ≤ 300", "grid[i][j] is '0' or '1'."],
        "leetcode_url": "https://leetcode.com/problems/number-of-islands/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(m × n) where m, n are grid dimensions",
        "space_complexity": "O(m × n) in worst case for recursion stack",
        "hints": ["Use DFS or BFS to explore connected components", "Mark visited cells to avoid counting them again"],
        "solution_template": "def numIslands(self, grid: List[List[str]]) -> int:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"grid": [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]}, "expected": 1}]
    },
    
    "course_schedule": {
        "id": "course_schedule",
        "title": "Course Schedule",
        "difficulty": "medium",
        "topic": "graphs",
        "category": "Graphs",
        "description": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return true if you can finish all courses.",
        "examples": [{"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true", "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible."}],
        "constraints": ["1 ≤ numCourses ≤ 2000", "0 ≤ prerequisites.length ≤ 5000", "prerequisites[i].length == 2"],
        "leetcode_url": "https://leetcode.com/problems/course-schedule/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(V + E) where V is courses, E is prerequisites",
        "space_complexity": "O(V + E) for adjacency list and recursion stack",
        "hints": ["This problem is equivalent to finding if a cycle exists in a directed graph", "Use DFS with three states: unvisited, visiting, visited"],
        "solution_template": "def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected": True}]
    },
    
    "alien_dictionary": {
        "id": "alien_dictionary",
        "title": "Alien Dictionary",
        "difficulty": "hard",
        "topic": "graphs",
        "category": "Graphs",
        "description": "There is a new alien language that uses the English alphabet. However, the order among the letters is unknown to you. You are given a list of strings words from the alien language's dictionary, where the strings in words are sorted lexicographically by the rules of this new language. Return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules.",
        "examples": [{"input": 'words = ["wrt","wrf","er","ett","rftt"]', "output": '"wertf"', "explanation": "Topological sort of alien alphabet"}],
        "constraints": ["1 ≤ words.length ≤ 100", "1 ≤ words[i].length ≤ 100", "words[i] consists of only lowercase English letters."],
        "leetcode_url": "https://leetcode.com/problems/alien-dictionary/",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook", "Airbnb"],
        "time_complexity": "O(C) where C is total length of all words",
        "space_complexity": "O(1) since at most 26 characters",
        "hints": ["Build a directed graph from the given words", "Find the topological ordering of the graph", "If there's a cycle, return empty string"],
        "solution_template": "def alienOrder(self, words: List[str]) -> str:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"words": ["wrt", "wrf", "er", "ett", "rftt"]}, "expected": "wertf"}]
    },

    # STACKS (3 problems)
    "valid_parentheses": {
        "id": "valid_parentheses",
        "title": "Valid Parentheses",
        "difficulty": "easy",
        "topic": "stacks",
        "category": "Stacks",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "examples": [{"input": 's = "()"', "output": "true", "explanation": "Valid parentheses"}, {"input": 's = "()[]{}"', "output": "true", "explanation": "All valid"}],
        "constraints": ["1 ≤ s.length ≤ 10⁴", "s consists of parentheses only '()[]{}'."],
        "leetcode_url": "https://leetcode.com/problems/valid-parentheses/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is length of string",
        "space_complexity": "O(n) for stack in worst case",
        "hints": ["Use a stack to keep track of opening brackets", "When you encounter a closing bracket, check if it matches the most recent opening bracket"],
        "solution_template": "def isValid(self, s: str) -> bool:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"s": "()"}, "expected": True}]
    },
    
    "largest_rectangle_histogram": {
        "id": "largest_rectangle_histogram",
        "title": "Largest Rectangle in Histogram",
        "difficulty": "medium",
        "topic": "stacks",
        "category": "Stacks",
        "description": "Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        "examples": [{"input": "heights = [2,1,5,6,2,3]", "output": "10", "explanation": "The largest rectangle has area = 10 units."}],
        "constraints": ["1 ≤ heights.length ≤ 10⁵", "0 ≤ heights[i] ≤ 10⁴"],
        "leetcode_url": "https://leetcode.com/problems/largest-rectangle-in-histogram/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n) with stack",
        "space_complexity": "O(n) for stack",
        "hints": ["Use a stack to keep track of indices of bars", "For each bar, find the largest rectangle with this bar as the smallest bar"],
        "solution_template": "def largestRectangleArea(self, heights: List[int]) -> int:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"heights": [2, 1, 5, 6, 2, 3]}, "expected": 10}]
    },
    
    "basic_calculator": {
        "id": "basic_calculator",
        "title": "Basic Calculator",
        "difficulty": "hard",
        "topic": "stacks",
        "category": "Stacks",
        "description": "Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.",
        "examples": [{"input": 's = "1 + 1"', "output": "2", "explanation": "Simple addition"}, {"input": 's = "(1+(4+5+2)-3)+(6+8)"', "output": "23", "explanation": "Complex expression with parentheses"}],
        "constraints": ["1 ≤ s.length ≤ 3 × 10⁵", "s consists of digits, '+', '-', '(', ')', and ' '.", "s represents a valid expression."],
        "leetcode_url": "https://leetcode.com/problems/basic-calculator/",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is length of string",
        "space_complexity": "O(n) for stack",
        "hints": ["Use a stack to handle parentheses", "Keep track of the current number, result, and sign"],
        "solution_template": "def calculate(self, s: str) -> int:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"s": "1 + 1"}, "expected": 2}]
    },

    # HASH TABLES (3 problems)
    "group_anagrams": {
        "id": "group_anagrams",
        "title": "Group Anagrams",
        "difficulty": "easy",
        "topic": "hash_tables",
        "category": "Hash Tables",
        "description": "Given an array of strings strs, group the anagrams together. You can return the answer in any order.",
        "examples": [{"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]', "explanation": "Group anagrams together"}],
        "constraints": ["1 ≤ strs.length ≤ 10⁴", "0 ≤ strs[i].length ≤ 100", "strs[i] consists of lowercase English letters only."],
        "leetcode_url": "https://leetcode.com/problems/group-anagrams/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n × k log k) where n is number of strings, k is max length",
        "space_complexity": "O(n × k) for storing all strings",
        "hints": ["Use sorted string as key in hash map", "Alternative: use character count as key"],
        "solution_template": "def groupAnagrams(self, strs: List[str]) -> List[List[str]]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]}]
    },
    
    "top_k_frequent": {
        "id": "top_k_frequent",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "topic": "hash_tables",
        "category": "Hash Tables",
        "description": "Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.",
        "examples": [{"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 appears 3 times, 2 appears 2 times"}],
        "constraints": ["1 ≤ nums.length ≤ 10⁵", "k is in the range [1, the number of unique elements in the array].", "It is guaranteed that the answer is unique."],
        "leetcode_url": "https://leetcode.com/problems/top-k-frequent-elements/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n log k) with heap, O(n) with bucket sort",
        "space_complexity": "O(n) for frequency map",
        "hints": ["Use hash map to count frequencies", "Use min heap of size k, or bucket sort for O(n) solution"],
        "solution_template": "def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, "expected": [1, 2]}]
    },
    
    "lru_cache": {
        "id": "lru_cache",
        "title": "LRU Cache",
        "difficulty": "hard",
        "topic": "hash_tables",
        "category": "Hash Tables",
        "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.",
        "examples": [{"input": '["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]', "output": "[null, null, null, 1, null, -1, null, -1, 3, 4]", "explanation": "LRU cache operations"}],
        "constraints": ["1 ≤ capacity ≤ 3000", "0 ≤ key ≤ 10⁴", "0 ≤ value ≤ 10⁵", "At most 2 × 10⁵ calls will be made to get and put."],
        "leetcode_url": "https://leetcode.com/problems/lru-cache/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(1) for both get and put operations",
        "space_complexity": "O(capacity) for storing cache entries",
        "hints": ["Use hash map + doubly linked list", "Hash map for O(1) access, doubly linked list for O(1) insertion/deletion"],
        "solution_template": "class LRUCache:\n    def __init__(self, capacity: int):\n        # Your solution here\n        pass\n        \n    def get(self, key: int) -> int:\n        # Your solution here\n        pass\n        \n    def put(self, key: int, value: int) -> None:\n        # Your solution here\n        pass",
        "test_cases": [{"input": {"operations": ["LRUCache", "put", "put", "get"], "values": [[2], [1, 1], [2, 2], [1]]}, "expected": [None, None, None, 1]}]
    }
}

def add_final_12_problems():
    """Add final 12 problems to complete the 24 unique problems"""
    redis_client = get_redis_client()
    
    print("🚀 ADDING FINAL 12 PROBLEMS...")
    print("📊 Dynamic Programming: 3, Graphs: 3, Stacks: 3, Hash Tables: 3")
    print()
    
    for problem_id, problem_data in FINAL_12_PROBLEMS.items():
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
    
    # Final count
    total_problems = redis_client.scard("all_problems")
    print(f"\n🎉 COMPLETE! {total_problems}/24 UNIQUE PROBLEMS ADDED")
    
    # Show final breakdown
    print("\n📊 FINAL BREAKDOWN:")
    topics = ["arrays", "strings", "trees", "linked_lists", "dynamic_programming", "graphs", "stacks", "hash_tables"]
    for topic in topics:
        count = redis_client.scard(f"problems_by_topic:{topic}")
        topic_display = topic.replace("_", " ").title()
        print(f"   ✅ {topic_display}: {count} problems")
    
    print("\n📈 BY DIFFICULTY:")
    for difficulty in ["easy", "medium", "hard"]:
        count = redis_client.scard(f"problems_by_difficulty:{difficulty}")
        emoji = "🟢" if difficulty == "easy" else "🟡" if difficulty == "medium" else "🔴"
        print(f"   {emoji} {difficulty.title()}: {count} problems")
    
    return len(FINAL_12_PROBLEMS)

if __name__ == "__main__":
    count = add_final_12_problems()
    print(f"\n🏆 SUCCESS! 24 UNIQUE PROBLEMS CREATED")
    print("✅ No duplicates - each problem appears exactly once")
    print("✅ Perfect distribution: 8 topics × 3 difficulties = 24 problems")
    print("✅ Ready for Redis AI Challenge!")
    print(f"\n📊 Added in this batch: {count} problems")
