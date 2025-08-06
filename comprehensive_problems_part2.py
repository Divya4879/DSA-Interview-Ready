#!/usr/bin/env python3
"""
Comprehensive DSA Problems Database - Part 2
Remaining 18 problems across 6 topics (Trees, Linked Lists, DP, Graphs, Stacks, Hash Tables)
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

# Part 2: Remaining 18 problems
COMPREHENSIVE_PROBLEMS_PART2 = {
    # TREES TOPIC
    "binary_tree_inorder": {
        "id": "binary_tree_inorder",
        "title": "Binary Tree Inorder Traversal",
        "difficulty": "easy",
        "topic": "trees",
        "category": "Trees",
        "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
        "examples": [
            {
                "input": "root = [1,null,2,3]",
                "output": "[1,3,2]",
                "explanation": ""
            },
            {
                "input": "root = []",
                "output": "[]",
                "explanation": ""
            },
            {
                "input": "root = [1]",
                "output": "[1]",
                "explanation": ""
            }
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 100].",
            "-100 ≤ Node.val ≤ 100"
        ],
        "leetcode_url": "https://leetcode.com/problems/binary-tree-inorder-traversal/",
        "companies": ["Microsoft", "Amazon", "Google", "Facebook"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(h) where h is height of tree",
        "hints": [
            "Can you solve it both recursively and iteratively?",
            "Use a stack for iterative approach"
        ],
        "solution_template": "def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:\n    # Approach 1: Recursive\n    # Approach 2: Iterative with stack\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"root": [1, None, 2, 3]}, "expected": [1, 3, 2]},
            {"input": {"root": []}, "expected": []},
            {"input": {"root": [1]}, "expected": [1]},
            {"input": {"root": [1, 2, 3, 4, 5]}, "expected": [4, 2, 5, 1, 3]}
        ]
    },

    "validate_bst": {
        "id": "validate_bst",
        "title": "Validate Binary Search Tree",
        "difficulty": "medium",
        "topic": "trees",
        "category": "Trees",
        "description": "Given the root of a binary tree, determine if it is a valid binary search tree (BST).\n\nA valid BST is defined as follows:\n\n• The left subtree of a node contains only nodes with keys less than the node's key.\n• The right subtree of a node contains only nodes with keys greater than the node's key.\n• Both the left and right subtrees must also be binary search trees.",
        "examples": [
            {
                "input": "root = [2,1,3]",
                "output": "true",
                "explanation": ""
            },
            {
                "input": "root = [5,1,4,null,null,3,6]",
                "output": "false",
                "explanation": "The root node's value is 5 but its right child's value is 4."
            }
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [1, 10⁴].",
            "-2³¹ ≤ Node.val ≤ 2³¹ - 1"
        ],
        "leetcode_url": "https://leetcode.com/problems/validate-binary-search-tree/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(h) where h is height of tree",
        "hints": [
            "Not all values in the left subtree are smaller than the root, and not all values in the right subtree are larger than the root.",
            "Use the definition of BST: left subtree of a node contains only nodes with keys less than the node's key.",
            "What if you do inorder traversal of the BST? What will you get? What if you do inorder traversal of the invalid BST?"
        ],
        "solution_template": "def isValidBST(self, root: Optional[TreeNode]) -> bool:\n    # Approach 1: Inorder traversal should be sorted\n    # Approach 2: Recursive with min/max bounds\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"root": [2, 1, 3]}, "expected": True},
            {"input": {"root": [5, 1, 4, None, None, 3, 6]}, "expected": False},
            {"input": {"root": [1]}, "expected": True},
            {"input": {"root": [10, 5, 15, None, None, 6, 20]}, "expected": False}
        ]
    },

    "serialize_deserialize_tree": {
        "id": "serialize_deserialize_tree",
        "title": "Serialize and Deserialize Binary Tree",
        "difficulty": "hard",
        "topic": "trees",
        "category": "Trees",
        "description": "Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.\n\nDesign an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.",
        "examples": [
            {
                "input": "root = [1,2,3,null,null,4,5]",
                "output": "[1,2,3,null,null,4,5]",
                "explanation": "This is just one way to serialize. You do not necessarily need to follow this format."
            },
            {
                "input": "root = []",
                "output": "[]",
                "explanation": ""
            }
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 10⁴].",
            "-1000 ≤ Node.val ≤ 1000"
        ],
        "leetcode_url": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "LinkedIn"],
        "time_complexity": "O(n) for both serialize and deserialize",
        "space_complexity": "O(n) for storing the tree",
        "hints": [
            "String split and join operations.",
            "Pre-order traversal is commonly used.",
            "Use a delimiter to separate values and a special marker for null nodes."
        ],
        "solution_template": "class Codec:\n    def serialize(self, root):\n        # Encode tree to string\n        pass\n        \n    def deserialize(self, data):\n        # Decode string to tree\n        pass",
        "test_cases": [
            {"input": {"root": [1, 2, 3, None, None, 4, 5]}, "expected": [1, 2, 3, None, None, 4, 5]},
            {"input": {"root": []}, "expected": []},
            {"input": {"root": [1]}, "expected": [1]},
            {"input": {"root": [1, 2]}, "expected": [1, 2]}
        ]
    },

    # LINKED LISTS TOPIC
    "reverse_linked_list": {
        "id": "reverse_linked_list",
        "title": "Reverse Linked List",
        "difficulty": "easy",
        "topic": "linked_lists",
        "category": "Linked Lists",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [
            {
                "input": "head = [1,2,3,4,5]",
                "output": "[5,4,3,2,1]",
                "explanation": ""
            },
            {
                "input": "head = [1,2]",
                "output": "[2,1]",
                "explanation": ""
            },
            {
                "input": "head = []",
                "output": "[]",
                "explanation": ""
            }
        ],
        "constraints": [
            "The number of nodes in the list is the range [0, 5000].",
            "-5000 ≤ Node.val ≤ 5000"
        ],
        "leetcode_url": "https://leetcode.com/problems/reverse-linked-list/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(1) iterative, O(n) recursive",
        "hints": [
            "A linked list can be reversed either iteratively or recursively. Could you implement both?",
            "For iterative approach, use three pointers: prev, curr, next"
        ],
        "solution_template": "def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n    # Approach 1: Iterative with three pointers\n    # Approach 2: Recursive\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"head": [1, 2, 3, 4, 5]}, "expected": [5, 4, 3, 2, 1]},
            {"input": {"head": [1, 2]}, "expected": [2, 1]},
            {"input": {"head": []}, "expected": []},
            {"input": {"head": [1]}, "expected": [1]}
        ]
    },

    "merge_two_sorted_lists": {
        "id": "merge_two_sorted_lists",
        "title": "Merge Two Sorted Lists",
        "difficulty": "medium",
        "topic": "linked_lists",
        "category": "Linked Lists",
        "description": "You are given the heads of two sorted linked lists list1 and list2.\n\nMerge the two lists in a sorted manner and return the head of the merged linked list.\n\nThe list should be made by splicing together the nodes of the first two lists.",
        "examples": [
            {
                "input": "list1 = [1,2,4], list2 = [1,3,4]",
                "output": "[1,1,2,3,4,4]",
                "explanation": ""
            },
            {
                "input": "list1 = [], list2 = []",
                "output": "[]",
                "explanation": ""
            },
            {
                "input": "list1 = [], list2 = [0]",
                "output": "[0]",
                "explanation": ""
            }
        ],
        "constraints": [
            "The number of nodes in both lists is in the range [0, 50].",
            "-100 ≤ Node.val ≤ 100",
            "Both list1 and list2 are sorted in non-decreasing order."
        ],
        "leetcode_url": "https://leetcode.com/problems/merge-two-sorted-lists/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(m + n) where m, n are lengths of lists",
        "space_complexity": "O(1) iterative, O(m + n) recursive",
        "hints": [
            "Use a dummy head to simplify the logic",
            "Compare values and link the smaller node"
        ],
        "solution_template": "def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n    # Use dummy head for easier implementation\n    # Compare values and link nodes\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "expected": [1, 1, 2, 3, 4, 4]},
            {"input": {"list1": [], "list2": []}, "expected": []},
            {"input": {"list1": [], "list2": [0]}, "expected": [0]},
            {"input": {"list1": [5], "list2": [1, 2, 4]}, "expected": [1, 2, 4, 5]}
        ]
    },

    "copy_list_random_pointer": {
        "id": "copy_list_random_pointer",
        "title": "Copy List with Random Pointer",
        "difficulty": "hard",
        "topic": "linked_lists",
        "category": "Linked Lists",
        "description": "A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.\n\nConstruct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointers of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.\n\nReturn the head of the copied linked list.",
        "examples": [
            {
                "input": "head = [[7,null],[13,0],[11,4],[10,2],[1,0]]",
                "output": "[[7,null],[13,0],[11,4],[10,2],[1,0]]",
                "explanation": ""
            },
            {
                "input": "head = [[1,1],[2,1]]",
                "output": "[[1,1],[2,1]]",
                "explanation": ""
            }
        ],
        "constraints": [
            "0 ≤ n ≤ 1000",
            "-10⁴ ≤ Node.val ≤ 10⁴",
            "Node.random is null or is pointing to some node in the linked list."
        ],
        "leetcode_url": "https://leetcode.com/problems/copy-list-with-random-pointer/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(n) for hash map or O(1) with interweaving",
        "hints": [
            "Just iterate the linked list and create copies of the nodes on the go. Since a node can be referenced from multiple nodes due to the random pointers, make sure you are not making multiple copies of the same node.",
            "You may want to use extra space to keep old node ---> new node mapping to prevent creating multiples copies of same node.",
            "We can avoid using extra space for old node ---> new node mapping, by tweaking the original linked list. Simply interweave the nodes of the old and copied list."
        ],
        "solution_template": "def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':\n    # Approach 1: Hash map to store old -> new mapping\n    # Approach 2: Interweave nodes to avoid extra space\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"head": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]}, "expected": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]},
            {"input": {"head": [[1, 1], [2, 1]]}, "expected": [[1, 1], [2, 1]]},
            {"input": {"head": []}, "expected": []},
            {"input": {"head": [[3, None]]}, "expected": [[3, None]]}
        ]
    },

    # DYNAMIC PROGRAMMING TOPIC
    "climbing_stairs": {
        "id": "climbing_stairs",
        "title": "Climbing Stairs",
        "difficulty": "easy",
        "topic": "dynamic_programming",
        "category": "Dynamic Programming",
        "description": "You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {
                "input": "n = 2",
                "output": "2",
                "explanation": "There are two ways to climb to the top.\n1. 1 step + 1 step\n2. 2 steps"
            },
            {
                "input": "n = 3",
                "output": "3",
                "explanation": "There are three ways to climb to the top.\n1. 1 step + 1 step + 1 step\n2. 1 step + 2 steps\n3. 2 steps + 1 step"
            }
        ],
        "constraints": [
            "1 ≤ n ≤ 45"
        ],
        "leetcode_url": "https://leetcode.com/problems/climbing-stairs/",
        "companies": ["Amazon", "Google", "Microsoft", "Adobe", "Apple"],
        "time_complexity": "O(n) with DP",
        "space_complexity": "O(1) with optimized space",
        "hints": [
            "To reach nth step, you could have come from (n-1)th step or (n-2)th step.",
            "So the number of ways to reach nth step is sum of ways to reach (n-1)th and (n-2)th step.",
            "This is actually a Fibonacci sequence!"
        ],
        "solution_template": "def climbStairs(self, n: int) -> int:\n    # This is Fibonacci sequence\n    # dp[i] = dp[i-1] + dp[i-2]\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"n": 2}, "expected": 2},
            {"input": {"n": 3}, "expected": 3},
            {"input": {"n": 1}, "expected": 1},
            {"input": {"n": 4}, "expected": 5},
            {"input": {"n": 5}, "expected": 8}
        ]
    },

    "longest_increasing_subsequence": {
        "id": "longest_increasing_subsequence",
        "title": "Longest Increasing Subsequence",
        "difficulty": "medium",
        "topic": "dynamic_programming",
        "category": "Dynamic Programming",
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.\n\nA subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of the remaining elements. For example, [3,6,2,7] is a subsequence of the array [0,3,1,6,2,2,7].",
        "examples": [
            {
                "input": "nums = [10,9,2,5,3,7,101,18]",
                "output": "4",
                "explanation": "The longest increasing subsequence is [2,3,7,18], therefore the length is 4."
            },
            {
                "input": "nums = [0,1,0,3,2,3]",
                "output": "4",
                "explanation": ""
            },
            {
                "input": "nums = [7,7,7,7,7,7,7]",
                "output": "1",
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ nums.length ≤ 2500",
            "-10⁴ ≤ nums[i] ≤ 10⁴"
        ],
        "leetcode_url": "https://leetcode.com/problems/longest-increasing-subsequence/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n²) DP, O(n log n) with binary search",
        "space_complexity": "O(n) for DP array",
        "hints": [
            "Define dp[i] as the length of the longest increasing subsequence ending at index i.",
            "For each i, check all previous elements j where nums[j] < nums[i].",
            "Can you optimize to O(n log n) using binary search?"
        ],
        "solution_template": "def lengthOfLIS(self, nums: List[int]) -> int:\n    # Approach 1: DP O(n²)\n    # Approach 2: Binary search O(n log n)\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, "expected": 4},
            {"input": {"nums": [0, 1, 0, 3, 2, 3]}, "expected": 4},
            {"input": {"nums": [7, 7, 7, 7, 7, 7, 7]}, "expected": 1},
            {"input": {"nums": [1, 3, 6, 7, 9, 4, 10, 5, 6]}, "expected": 6}
        ]
    },

    "word_break": {
        "id": "word_break",
        "title": "Word Break",
        "difficulty": "hard",
        "topic": "dynamic_programming",
        "category": "Dynamic Programming",
        "description": "Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.\n\nNote that the same word in the dictionary may be reused multiple times in the segmentation.",
        "examples": [
            {
                "input": 's = "leetcode", wordDict = ["leet","code"]',
                "output": "true",
                "explanation": 'Return true because "leetcode" can be segmented as "leet code".'
            },
            {
                "input": 's = "applepenapple", wordDict = ["apple","pen"]',
                "output": "true",
                "explanation": 'Return true because "applepenapple" can be segmented as "apple pen apple".'
            },
            {
                "input": 's = "catsandog", wordDict = ["cats","dog","sand","and","cat"]',
                "output": "false",
                "explanation": ""
            }
        ],
        "constraints": [
            "1 ≤ s.length ≤ 300",
            "1 ≤ wordDict.length ≤ 1000",
            "1 ≤ wordDict[i].length ≤ 20",
            "s and wordDict[i] consist of only lowercase English letters.",
            "All the strings of wordDict are unique."
        ],
        "leetcode_url": "https://leetcode.com/problems/word-break/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "Apple"],
        "time_complexity": "O(n² + m) where n is length of s, m is total length of words",
        "space_complexity": "O(n + m) for DP array and word set",
        "hints": [
            "Think about the valid starting points.",
            "dp[i] represents whether s[0...i-1] can be segmented into words from the dictionary.",
            "For each position i, check if there exists a j such that dp[j] is true and s[j...i-1] is in wordDict."
        ],
        "solution_template": "def wordBreak(self, s: str, wordDict: List[str]) -> bool:\n    # DP approach: dp[i] = can s[0:i] be segmented\n    # For each position, check all possible word endings\n    \n    # Your solution here\n    pass",
        "test_cases": [
            {"input": {"s": "leetcode", "wordDict": ["leet", "code"]}, "expected": True},
            {"input": {"s": "applepenapple", "wordDict": ["apple", "pen"]}, "expected": True},
            {"input": {"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, "expected": False},
            {"input": {"s": "cars", "wordDict": ["car", "ca", "rs"]}, "expected": True}
        ]
    }
}

def add_problems_part2_to_redis():
    """Add part 2 problems to Redis"""
    redis_client = get_redis_client()
    
    print("🚀 Adding comprehensive problems part 2 to Redis...")
    
    for problem_id, problem_data in COMPREHENSIVE_PROBLEMS_PART2.items():
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
    
    print(f"\n🎉 Successfully added {len(COMPREHENSIVE_PROBLEMS_PART2)} problems!")

if __name__ == "__main__":
    add_problems_part2_to_redis()
