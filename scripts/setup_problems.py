#!/usr/bin/env python3
"""
Production setup script for DSA Interview Platform
Creates essential problems and Redis indexes for deployment
"""

import redis
import json
import os
import sys
from datetime import datetime

def setup_redis_connection():
    """Setup Redis connection with environment variables"""
    try:
        return redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            password=os.getenv('REDIS_PASSWORD', ''),
            username=os.getenv('REDIS_USERNAME', 'default'),
            decode_responses=True,
            ssl=False,
            socket_timeout=30
        )
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return None

def create_search_indexes(redis_client):
    """Create Redis Search indexes"""
    try:
        # Drop existing indexes if they exist
        try:
            redis_client.execute_command('FT.DROPINDEX', 'problem_idx')
        except:
            pass
            
        # Create problem search index
        redis_client.execute_command(
            'FT.CREATE', 'problem_idx',
            'ON', 'HASH',
            'PREFIX', '1', 'problem:',
            'SCHEMA',
            'title', 'TEXT', 'WEIGHT', '2.0',
            'description', 'TEXT',
            'difficulty', 'TAG',
            'topic', 'TAG'
        )
        print("✅ Search indexes created successfully")
        return True
    except Exception as e:
        print(f"⚠️ Search index creation failed: {e}")
        return False

def create_essential_problems(redis_client):
    """Create essential DSA problems for production"""
    problems = [
        {
            'id': 'two_sum',
            'title': 'Two Sum',
            'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
            'difficulty': 'easy',
            'topic': 'arrays',
            'solution_template': 'def two_sum(nums, target):\n    # Your solution here\n    pass',
            'companies': ['Google', 'Amazon', 'Microsoft'],
            'leetcode_link': 'https://leetcode.com/problems/two-sum/'
        },
        {
            'id': 'reverse_linked_list',
            'title': 'Reverse Linked List',
            'description': 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
            'difficulty': 'easy',
            'topic': 'linked-lists',
            'solution_template': 'def reverse_list(head):\n    # Your solution here\n    pass',
            'companies': ['Facebook', 'Apple', 'Netflix'],
            'leetcode_link': 'https://leetcode.com/problems/reverse-linked-list/'
        },
        {
            'id': 'valid_parentheses',
            'title': 'Valid Parentheses',
            'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.',
            'difficulty': 'easy',
            'topic': 'stacks',
            'solution_template': 'def is_valid(s):\n    # Your solution here\n    pass',
            'companies': ['Google', 'Microsoft', 'Amazon'],
            'leetcode_link': 'https://leetcode.com/problems/valid-parentheses/'
        },
        {
            'id': 'binary_tree_inorder',
            'title': 'Binary Tree Inorder Traversal',
            'description': 'Given the root of a binary tree, return the inorder traversal of its nodes\' values.',
            'difficulty': 'easy',
            'topic': 'trees',
            'solution_template': 'def inorder_traversal(root):\n    # Your solution here\n    pass',
            'companies': ['Facebook', 'Google', 'Amazon'],
            'leetcode_link': 'https://leetcode.com/problems/binary-tree-inorder-traversal/'
        },
        {
            'id': 'maximum_subarray',
            'title': 'Maximum Subarray',
            'description': 'Given an integer array nums, find the contiguous subarray which has the largest sum and return its sum.',
            'difficulty': 'medium',
            'topic': 'dynamic-programming',
            'solution_template': 'def max_subarray(nums):\n    # Your solution here\n    pass',
            'companies': ['Amazon', 'Microsoft', 'Apple'],
            'leetcode_link': 'https://leetcode.com/problems/maximum-subarray/'
        }
    ]
    
    try:
        for problem in problems:
            problem_key = f"problem:{problem['id']}"
            redis_client.hset(problem_key, mapping={
                'id': problem['id'],
                'title': problem['title'],
                'description': problem['description'],
                'difficulty': problem['difficulty'],
                'topic': problem['topic'],
                'solution_template': problem['solution_template'],
                'companies': ','.join(problem['companies']),
                'leetcode_link': problem.get('leetcode_link', ''),
                'created_at': datetime.now().isoformat()
            })
            
            # Add to topic and difficulty sets
            redis_client.sadd('topics', problem['topic'])
            redis_client.sadd('difficulties', problem['difficulty'])
        
        print(f"✅ Created {len(problems)} essential problems")
        return True
    except Exception as e:
        print(f"❌ Problem creation failed: {e}")
        return False

def setup_platform_stats(redis_client):
    """Initialize platform statistics"""
    try:
        redis_client.hset('platform_stats', mapping={
            'total_problems': 5,
            'total_users': 0,
            'total_submissions': 0,
            'last_updated': datetime.now().isoformat()
        })
        print("✅ Platform stats initialized")
        return True
    except Exception as e:
        print(f"⚠️ Platform stats setup failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up DSA Interview Platform...")
    print("=" * 50)
    
    # Setup Redis connection
    redis_client = setup_redis_connection()
    if not redis_client:
        print("❌ Setup failed: Could not connect to Redis")
        sys.exit(1)
    
    try:
        # Test connection
        redis_client.ping()
        print("✅ Redis connection successful")
    except Exception as e:
        print(f"❌ Redis connection test failed: {e}")
        sys.exit(1)
    
    # Create search indexes
    create_search_indexes(redis_client)
    
    # Create essential problems
    if not create_essential_problems(redis_client):
        print("⚠️ Warning: Problem creation had issues")
    
    # Setup platform stats
    setup_platform_stats(redis_client)
    
    print("\n🎉 DSA Interview Platform setup completed!")
    print("✅ Ready for production deployment")

if __name__ == "__main__":
    main()
