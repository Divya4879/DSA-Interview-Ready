#!/usr/bin/env python3
"""
Add Trees and Linked Lists problems (6 more unique problems)
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

# Trees and Linked Lists problems (6 unique problems)
TREES_LINKEDLISTS_PROBLEMS = {
    # TREES (3 problems)
    "binary_tree_inorder": {
        "id": "binary_tree_inorder",
        "title": "Binary Tree Inorder Traversal",
        "difficulty": "easy",
        "topic": "trees",
        "category": "Trees",
        "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
        "examples": [{"input": "root = [1,null,2,3]", "output": "[1,3,2]", "explanation": "Inorder traversal: left, root, right"}],
        "constraints": ["The number of nodes in the tree is in the range [0, 100].", "-100 ≤ Node.val ≤ 100"],
        "leetcode_url": "https://leetcode.com/problems/binary-tree-inorder-traversal/",
        "companies": ["Microsoft", "Amazon", "Google", "Facebook"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(h) where h is height of tree",
        "hints": ["Can you solve it both recursively and iteratively?", "Use a stack for iterative approach"],
        "solution_template": "def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"root": [1, None, 2, 3]}, "expected": [1, 3, 2]}]
    },
    
    "validate_bst": {
        "id": "validate_bst",
        "title": "Validate Binary Search Tree",
        "difficulty": "medium",
        "topic": "trees",
        "category": "Trees",
        "description": "Given the root of a binary tree, determine if it is a valid binary search tree (BST).",
        "examples": [{"input": "root = [2,1,3]", "output": "true", "explanation": "Valid BST"}, {"input": "root = [5,1,4,null,null,3,6]", "output": "false", "explanation": "Invalid BST"}],
        "constraints": ["The number of nodes in the tree is in the range [1, 10⁴].", "-2³¹ ≤ Node.val ≤ 2³¹ - 1"],
        "leetcode_url": "https://leetcode.com/problems/validate-binary-search-tree/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(h) where h is height of tree",
        "hints": ["Use the definition of BST with min/max bounds", "Inorder traversal should be sorted"],
        "solution_template": "def isValidBST(self, root: Optional[TreeNode]) -> bool:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"root": [2, 1, 3]}, "expected": True}]
    },
    
    "serialize_deserialize_tree": {
        "id": "serialize_deserialize_tree",
        "title": "Serialize and Deserialize Binary Tree",
        "difficulty": "hard",
        "topic": "trees",
        "category": "Trees",
        "description": "Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work.",
        "examples": [{"input": "root = [1,2,3,null,null,4,5]", "output": "[1,2,3,null,null,4,5]", "explanation": "Serialize and deserialize the tree"}],
        "constraints": ["The number of nodes in the tree is in the range [0, 10⁴].", "-1000 ≤ Node.val ≤ 1000"],
        "leetcode_url": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/",
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "LinkedIn"],
        "time_complexity": "O(n) for both serialize and deserialize",
        "space_complexity": "O(n) for storing the tree",
        "hints": ["Use pre-order traversal", "Use a delimiter to separate values", "Use a special marker for null nodes"],
        "solution_template": "class Codec:\n    def serialize(self, root):\n        # Your solution here\n        pass\n        \n    def deserialize(self, data):\n        # Your solution here\n        pass",
        "test_cases": [{"input": {"root": [1, 2, 3, None, None, 4, 5]}, "expected": [1, 2, 3, None, None, 4, 5]}]
    },

    # LINKED LISTS (3 problems)
    "reverse_linked_list": {
        "id": "reverse_linked_list",
        "title": "Reverse Linked List",
        "difficulty": "easy",
        "topic": "linked_lists",
        "category": "Linked Lists",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]", "explanation": "Reverse the linked list"}],
        "constraints": ["The number of nodes in the list is the range [0, 5000].", "-5000 ≤ Node.val ≤ 5000"],
        "leetcode_url": "https://leetcode.com/problems/reverse-linked-list/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(1) iterative, O(n) recursive",
        "hints": ["Use three pointers: prev, curr, next", "A linked list can be reversed either iteratively or recursively"],
        "solution_template": "def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"head": [1, 2, 3, 4, 5]}, "expected": [5, 4, 3, 2, 1]}]
    },
    
    "merge_two_sorted_lists": {
        "id": "merge_two_sorted_lists",
        "title": "Merge Two Sorted Lists",
        "difficulty": "medium",
        "topic": "linked_lists",
        "category": "Linked Lists",
        "description": "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists in a sorted manner and return the head of the merged linked list.",
        "examples": [{"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]", "explanation": "Merge two sorted lists"}],
        "constraints": ["The number of nodes in both lists is in the range [0, 50].", "-100 ≤ Node.val ≤ 100", "Both list1 and list2 are sorted in non-decreasing order."],
        "leetcode_url": "https://leetcode.com/problems/merge-two-sorted-lists/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook", "Apple"],
        "time_complexity": "O(m + n) where m, n are lengths of lists",
        "space_complexity": "O(1) iterative, O(m + n) recursive",
        "hints": ["Use a dummy head to simplify the logic", "Compare values and link the smaller node"],
        "solution_template": "def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "expected": [1, 1, 2, 3, 4, 4]}]
    },
    
    "copy_list_random_pointer": {
        "id": "copy_list_random_pointer",
        "title": "Copy List with Random Pointer",
        "difficulty": "hard",
        "topic": "linked_lists",
        "category": "Linked Lists",
        "description": "A linked list of length n is given such that each node contains an additional random pointer. Construct a deep copy of the list.",
        "examples": [{"input": "head = [[7,null],[13,0],[11,4],[10,2],[1,0]]", "output": "[[7,null],[13,0],[11,4],[10,2],[1,0]]", "explanation": "Deep copy with random pointers"}],
        "constraints": ["0 ≤ n ≤ 1000", "-10⁴ ≤ Node.val ≤ 10⁴", "Node.random is null or is pointing to some node in the linked list."],
        "leetcode_url": "https://leetcode.com/problems/copy-list-with-random-pointer/",
        "companies": ["Amazon", "Microsoft", "Google", "Facebook"],
        "time_complexity": "O(n) where n is number of nodes",
        "space_complexity": "O(n) for hash map or O(1) with interweaving",
        "hints": ["Use hash map to store old -> new mapping", "You can avoid extra space by interweaving nodes"],
        "solution_template": "def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':\n    # Your solution here\n    pass",
        "test_cases": [{"input": {"head": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]}, "expected": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]}]
    }
}

def add_trees_linkedlists():
    """Add Trees and Linked Lists problems"""
    redis_client = get_redis_client()
    
    print("🌳 ADDING TREES AND LINKED LISTS PROBLEMS...")
    print("📊 Adding 6 more unique problems (Trees: 3, Linked Lists: 3)")
    print()
    
    for problem_id, problem_data in TREES_LINKEDLISTS_PROBLEMS.items():
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
    
    # Check current totals
    total_problems = redis_client.scard("all_problems")
    print(f"\n📊 PROGRESS: {total_problems}/24 problems added")
    print("✅ Trees and Linked Lists completed")
    
    return len(TREES_LINKEDLISTS_PROBLEMS)

if __name__ == "__main__":
    count = add_trees_linkedlists()
    print(f"\n🎯 CURRENT STATUS:")
    print("✅ Arrays: 3 problems")
    print("✅ Strings: 3 problems") 
    print("✅ Trees: 3 problems")
    print("✅ Linked Lists: 3 problems")
    print("🔄 Remaining: Dynamic Programming, Graphs, Stacks, Hash Tables (12 problems)")
    print(f"\n📊 Total added in this batch: {count} problems")
