#!/usr/bin/env python3
"""
Comprehensive DSA Problems Database - Part 3 (Final)
Final 9 problems: Graphs, Stacks, Hash Tables (3 each)
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

# Part 3: Final 9 problems
COMPREHENSIVE_PROBLEMS_PART3 = {
    # GRAPHS TOPIC
    "number_of_islands": {
        "id": "number_of_islands",
        "title": "Number of Islands",
        "difficulty": "easy",
        "topic": "graphs",
        "category": "Graphs",
        "description": "Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.",
        "examples": [
            {
                "input": 'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]',
                "output": "1",
                "explanation": ""
            },
            {
                "input": 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]',
                "output": "3",
                "explanation": ""
            }
        ],
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 ≤ m, n ≤ 300",
            "grid[i][j] is '0' or '1'."
        ],
        "leetcode_url": "https://leetcode.com/problems/number-of-islands/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(m × n) where m, n are grid dimensions",
        "space_complexity": "O(m × n) in worst case for recursion stack",
        "hints": [
            "Use DFS or BFS to explore connected components",
            "Mark visited cells to avoid counting them again"
        ],
        "solution_template": "def numIslands(self, grid: List[List[str]]) -> int:\n    # DFS or BFS to find connected components\n    # Mark visited cells as '0' or use visited set\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"grid": [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]}, "expected": 1},
            {"input": {"grid": [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]}, "expected": 3},
            {"input": {"grid": [["1"]]}, "expected": 1},
            {"input": {"grid": [["0"]]}, "expected": 0}
        ]
    },

    "course_schedule": {
        "id": "course_schedule",
        "title": "Course Schedule",
        "difficulty": "medium",
        "topic": "graphs",
        "category": "Graphs",
        "description": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.\n\nFor example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.\n\nReturn true if you can finish all courses. Otherwise, return false.",
        "examples": [
            {
                "input": "numCourses = 2, prerequisites = [[1,0]]",
                "output": "true",
                "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible."
            },
            {
                "input": "numCourses = 2, prerequisites = [[1,0],[0,1]]",
                "output": "false",
                "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible."
            }
        ],
        "constraints": [
            "1 ≤ numCourses ≤ 2000",
            "0 ≤ prerequisites.length ≤ 5000",
            "prerequisites[i].length == 2",
            "0 ≤ ai, bi < numCourses",
            "All the pairs prerequisites[i] are unique."
        ],
        "leetcode_url": "https://leetcode.com/problems/course-schedule/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(V + E) where V is courses, E is prerequisites",
        "space_complexity": "O(V + E) for adjacency list and recursion stack",
        "hints": [
            "This problem is equivalent to finding if a cycle exists in a directed graph.",
            "Use DFS with three states: unvisited, visiting, visited",
            "Topological sort can also solve this problem"
        ],
        "solution_template": "def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:\n    # Build adjacency list\n    # Use DFS to detect cycles\n    # Three states: white (unvisited), gray (visiting), black (visited)\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected": True},
            {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected": False},
            {"input": {"numCourses": 1, "prerequisites": []}, "expected": True},
            {"input": {"numCourses": 3, "prerequisites": [[1, 0], [2, 1]]}, "expected": True}
        ]
    },

    "alien_dictionary": {
        "id": "alien_dictionary",
        "title": "Alien Dictionary",
        "difficulty": "hard",
        "topic": "graphs",
        "category": "Graphs",
        "description": "There is a new alien language that uses the English alphabet. However, the order among the letters is unknown to you.\n\nYou are given a list of strings words from the alien language's dictionary, where the strings in words are sorted lexicographically by the rules of this new language.\n\nReturn a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there is no solution, return \"\". If there are multiple solutions, return any of them.",
        "examples": [
            {
                "input": 'words = ["wrt","wrf","er","ett","rftt"]',
                "output": '"wertf"',
                "explanation": ""
            },
            {
                "input": 'words = ["z","x"]',
                "output": '"zx"',
                "explanation": ""
            },
            {
                "input": 'words = ["z","x","z"]',
                "output": '""',
                "explanation": "The order is invalid, so return \"\"."
            }
        ],
        "constraints": [
            "1 ≤ words.length ≤ 100",
            "1 ≤ words[i].length ≤ 100",
            "words[i] consists of only lowercase English letters."
        ],
        "leetcode_url": "https://leetcode.com/problems/alien-dictionary/",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook", "Airbnb"],
        "time_complexity": "O(C) where C is total length of all words",
        "space_complexity": "O(1) since at most 26 characters",
        "hints": [
            "Build a directed graph from the given words",
            "Find the topological ordering of the graph",
            "If there's a cycle, return empty string"
        ],
        "solution_template": "def alienOrder(self, words: List[str]) -> str:\n    # Build graph by comparing adjacent words\n    # Use topological sort (Kahn's algorithm or DFS)\n    # Handle edge cases: cycles, invalid orderings\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"words": ["wrt", "wrf", "er", "ett", "rftt"]}, "expected": "wertf"},
            {"input": {"words": ["z", "x"]}, "expected": "zx"},
            {"input": {"words": ["z", "x", "z"]}, "expected": ""},
            {"input": {"words": ["abc", "ab"]}, "expected": ""}
        ]
    },

    # STACKS TOPIC
    "valid_parentheses": {
        "id": "valid_parentheses",
        "title": "Valid Parentheses",
        "difficulty": "easy",
        "topic": "stacks",
        "category": "Stacks",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "examples": [
            {
                "input": 's = "()"',
                "output": "true",
                "explanation": ""
            },
            {
                "input": 's = "()[]{}"',
                "output": "true",
                "explanation": ""
            },
            {
                "input": 's = "(]"',
                "output": "false",
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ s.length ≤ 10⁴",
            "s consists of parentheses only '()[]{}'."
        ],
        "leetcode_url": "https://leetcode.com/problems/valid-parentheses/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is length of string",
        "space_complexity": "O(n) for stack in worst case",
        "hints": [
            "Use a stack to keep track of opening brackets",
            "When you encounter a closing bracket, check if it matches the most recent opening bracket"
        ],
        "solution_template": "def isValid(self, s: str) -> bool:\n    # Use stack to track opening brackets\n    # For each closing bracket, check if it matches top of stack\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"s": "()"}, "expected": True},
            {"input": {"s": "()[]{}"}, "expected": True},
            {"input": {"s": "(]"}, "expected": False},
            {"input": {"s": "([)]"}, "expected": False},
            {"input": {"s": "{[]}"}, "expected": True}
        ]
    },

    "largest_rectangle_histogram": {
        "id": "largest_rectangle_histogram",
        "title": "Largest Rectangle in Histogram",
        "difficulty": "medium",
        "topic": "stacks",
        "category": "Stacks",
        "description": "Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        "examples": [
            {
                "input": "heights = [2,1,5,6,2,3]",
                "output": "10",
                "explanation": "The above is a histogram where width of each bar is 1. The largest rectangle is shown in the red area, which has an area = 10 units."
            },
            {
                "input": "heights = [2,4]",
                "output": "4",
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ heights.length ≤ 10⁵",
            "0 ≤ heights[i] ≤ 10⁴"
        ],
        "leetcode_url": "https://leetcode.com/problems/largest-rectangle-in-histogram/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n) with stack",
        "space_complexity": "O(n) for stack",
        "hints": [
            "Use a stack to keep track of indices of bars",
            "For each bar, find the largest rectangle with this bar as the smallest bar",
            "When current bar is smaller than stack top, calculate area with stack top as smallest bar"
        ],
        "solution_template": "def largestRectangleArea(self, heights: List[int]) -> int:\n    # Use stack to store indices\n    # For each bar, calculate max area with this bar as height\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"heights": [2, 1, 5, 6, 2, 3]}, "expected": 10},
            {"input": {"heights": [2, 4]}, "expected": 4},
            {"input": {"heights": [1]}, "expected": 1},
            {"input": {"heights": [0]}, "expected": 0},
            {"input": {"heights": [2, 2, 2, 2]}, "expected": 8}
        ]
    },

    "basic_calculator": {
        "id": "basic_calculator",
        "title": "Basic Calculator",
        "difficulty": "hard",
        "topic": "stacks",
        "category": "Stacks",
        "description": "Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.\n\nNote: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().",
        "examples": [
            {
                "input": 's = "1 + 1"',
                "output": "2",
                "explanation": ""
            },
            {
                "input": 's = " 2-1 + 2 "',
                "output": "3",
                "explanation": ""
            },
            {
                "input": 's = "(1+(4+5+2)-3)+(6+8)"',
                "output": "23",
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ s.length ≤ 3 × 10⁵",
            "s consists of digits, '+', '-', '(', ')', and ' '.",
            "s represents a valid expression.",
            "'+' is not used as a unary operation.",
            "'-' could be used as a unary operation and in this case, it will not be used directly after a '+' or another '-'.",
            "There will be no two consecutive operators in the input.",
            "Every number and running calculation will fit in a signed 32-bit integer."
        ],
        "leetcode_url": "https://leetcode.com/problems/basic-calculator/",
        "companies": ["Google", "Amazon", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is length of string",
        "space_complexity": "O(n) for stack",
        "hints": [
            "Use a stack to handle parentheses",
            "Keep track of the current number, result, and sign",
            "When encountering '(', push current result and sign to stack"
        ],
        "solution_template": "def calculate(self, s: str) -> int:\n    # Use stack for parentheses\n    # Track current number, result, and sign\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"s": "1 + 1"}, "expected": 2},
            {"input": {"s": " 2-1 + 2 "}, "expected": 3},
            {"input": {"s": "(1+(4+5+2)-3)+(6+8)"}, "expected": 23},
            {"input": {"s": "- (3 + (4 + 5))"}, "expected": -12}
        ]
    },

    # HASH TABLES TOPIC
    "group_anagrams": {
        "id": "group_anagrams",
        "title": "Group Anagrams",
        "difficulty": "easy",
        "topic": "hash_tables",
        "category": "Hash Tables",
        "description": "Given an array of strings strs, group the anagrams together. You can return the answer in any order.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": [
            {
                "input": 'strs = ["eat","tea","tan","ate","nat","bat"]',
                "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]',
                "explanation": ""
            },
            {
                "input": 'strs = [""]',
                "output": '[[""]]',
                "explanation": ""
            },
            {
                "input": 'strs = ["a"]',
                "output": '[["a"]]',
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ strs.length ≤ 10⁴",
            "0 ≤ strs[i].length ≤ 100",
            "strs[i] consists of lowercase English letters only."
        ],
        "leetcode_url": "https://leetcode.com/problems/group-anagrams/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n × k log k) where n is number of strings, k is max length",
        "space_complexity": "O(n × k) for storing all strings",
        "hints": [
            "Use sorted string as key in hash map",
            "Alternative: use character count as key"
        ],
        "solution_template": "def groupAnagrams(self, strs: List[str]) -> List[List[str]]:\n    # Use hash map with sorted string as key\n    # Or use character frequency as key\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}, "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]},
            {"input": {"strs": [""]}, "expected": [[""]]},
            {"input": {"strs": ["a"]}, "expected": [["a"]]},
            {"input": {"strs": ["abc", "bca", "cab", "xyz"]}, "expected": [["abc", "bca", "cab"], ["xyz"]]}
        ]
    },

    "top_k_frequent": {
        "id": "top_k_frequent",
        "title": "Top K Frequent Elements",
        "difficulty": "medium",
        "topic": "hash_tables",
        "category": "Hash Tables",
        "description": "Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.",
        "examples": [
            {
                "input": "nums = [1,1,1,2,2,3], k = 2",
                "output": "[1,2]",
                "explanation": ""
            },
            {
                "input": "nums = [1], k = 1",
                "output": "[1]",
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ nums.length ≤ 10⁵",
            "k is in the range [1, the number of unique elements in the array].",
            "It is guaranteed that the answer is unique."
        ],
        "leetcode_url": "https://leetcode.com/problems/top-k-frequent-elements/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n log k) with heap, O(n) with bucket sort",
        "space_complexity": "O(n) for frequency map",
        "hints": [
            "Use hash map to count frequencies",
            "Use min heap of size k, or bucket sort for O(n) solution"
        ],
        "solution_template": "def topKFrequent(self, nums: List[int], k: int) -> List[int]:\n    # Count frequencies with hash map\n    # Use heap or bucket sort to find top k\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"nums": [1, 1, 1, 2, 2, 3], "k": 2}, "expected": [1, 2]},
            {"input": {"nums": [1], "k": 1}, "expected": [1]},
            {"input": {"nums": [4, 1, -1, 2, -1, 2, 3], "k": 2}, "expected": [-1, 2]},
            {"input": {"nums": [1, 2], "k": 2}, "expected": [1, 2]}
        ]
    },

    "lru_cache": {
        "id": "lru_cache",
        "title": "LRU Cache",
        "difficulty": "hard",
        "topic": "hash_tables",
        "category": "Hash Tables",
        "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement the LRUCache class:\n\n• LRUCache(int capacity) Initialize the LRU cache with positive size capacity.\n• int get(int key) Return the value of the key if the key exists, otherwise return -1.\n• void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.\n\nThe functions get and put must each run in O(1) average time complexity.",
        "examples": [
            {
                "input": '["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]',
                "output": "[null, null, null, 1, null, -1, null, -1, 3, 4]",
                "explanation": "LRUCache lRUCache = new LRUCache(2);\nlRUCache.put(1, 1); // cache is {1=1}\nlRUCache.put(2, 2); // cache is {1=1, 2=2}\nlRUCache.get(1);    // return 1\nlRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}\nlRUCache.get(2);    // returns -1 (not found)\nlRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}\nlRUCache.get(1);    // return -1 (not found)\nlRUCache.get(3);    // return 3\nlRUCache.get(4);    // return 4"
            }
        ],
        "constraints": [
            "1 ≤ capacity ≤ 3000",
            "0 ≤ key ≤ 10⁴",
            "0 ≤ value ≤ 10⁵",
            "At most 2 × 10⁵ calls will be made to get and put."
        ],
        "leetcode_url": "https://leetcode.com/problems/lru-cache/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(1) for both get and put operations",
        "space_complexity": "O(capacity) for storing cache entries",
        "hints": [
            "Use hash map + doubly linked list",
            "Hash map for O(1) access, doubly linked list for O(1) insertion/deletion",
            "Keep track of head (most recent) and tail (least recent)"
        ],
        "solution_template": "class LRUCache:\n    def __init__(self, capacity: int):\n        # Use hash map + doubly linked list\n        pass\n        \n    def get(self, key: int) -> int:\n        # Move to front if exists\n        pass\n        \n    def put(self, key: int, value: int) -> None:\n        # Add/update and move to front\n        # Evict LRU if over capacity\n        pass",
        "test_cases": [
            {"input": {"operations": ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"], "values": [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]}, "expected": [None, None, None, 1, None, -1, None, -1, 3, 4]}
        ]
    }
}

def add_problems_part3_to_redis():
    """Add part 3 (final) problems to Redis"""
    redis_client = get_redis_client()
    
    print("🚀 Adding comprehensive problems part 3 (final) to Redis...")
    
    for problem_id, problem_data in COMPREHENSIVE_PROBLEMS_PART3.items():
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
    
    print(f"\n🎉 Successfully added {len(COMPREHENSIVE_PROBLEMS_PART3)} problems!")

if __name__ == "__main__":
    add_problems_part3_to_redis()
