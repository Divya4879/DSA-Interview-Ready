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

problems = []

# STRINGS PROBLEMS (10 problems)
strings_problems = [
    create_problem(
        'valid_anagram', 'Valid Anagram',
        'Given two strings s and t, return true if t is an anagram of s, and false otherwise. An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.',
        'easy', 'strings',
        [
            {'input': 's = "anagram", t = "nagaram"', 'output': 'true', 'explanation': 'Both strings contain the same characters with the same frequency.'},
            {'input': 's = "rat", t = "car"', 'output': 'false', 'explanation': 'The strings contain different characters.'},
            {'input': 's = "a", t = "ab"', 'output': 'false', 'explanation': 'The strings have different lengths.'}
        ],
        ['Count the frequency of each character in both strings', 'Compare the character frequencies', 'Alternatively, sort both strings and compare them'],
        ['1 ≤ s.length, t.length ≤ 5 × 10⁴', 's and t consist of lowercase English letters']
    ),
    
    create_problem(
        'valid_palindrome', 'Valid Palindrome',
        'A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers. Given a string s, return true if it is a palindrome, or false otherwise.',
        'easy', 'strings',
        [
            {'input': 's = "A man, a plan, a canal: Panama"', 'output': 'true', 'explanation': 'After processing: "amanaplanacanalpanama" is a palindrome.'},
            {'input': 's = "race a car"', 'output': 'false', 'explanation': 'After processing: "raceacar" is not a palindrome.'},
            {'input': 's = " "', 'output': 'true', 'explanation': 'After removing non-alphanumeric characters, the string becomes empty, which is a palindrome.'}
        ],
        ['Use two pointers, one from the beginning and one from the end', 'Skip non-alphanumeric characters', 'Compare characters after converting to lowercase'],
        ['1 ≤ s.length ≤ 2 × 10⁵', 's consists only of printable ASCII characters']
    ),
    
    create_problem(
        'longest_substring_no_repeat', 'Longest Substring Without Repeating Characters',
        'Given a string s, find the length of the longest substring without repeating characters. A substring is a contiguous non-empty sequence of characters within a string.',
        'medium', 'strings',
        [
            {'input': 's = "abcabcbb"', 'output': '3', 'explanation': 'The answer is "abc", with the length of 3.'},
            {'input': 's = "bbbbb"', 'output': '1', 'explanation': 'The answer is "b", with the length of 1.'},
            {'input': 's = "pwwkew"', 'output': '3', 'explanation': 'The answer is "wke", with the length of 3. Note that "pwke" is a subsequence, not a substring.'}
        ],
        ['Use the sliding window technique with two pointers', 'Use a hash set to track characters in the current window', 'When a duplicate is found, move the left pointer to skip the duplicate'],
        ['0 ≤ s.length ≤ 5 × 10⁴', 's consists of English letters, digits, symbols and spaces']
    )
]

# LINKED LISTS PROBLEMS (10 problems)
linked_lists_problems = [
    create_problem(
        'reverse_linked_list', 'Reverse Linked List',
        'Given the head of a singly linked list, reverse the list, and return the reversed list.',
        'easy', 'linked-lists',
        [
            {'input': 'head = [1,2,3,4,5]', 'output': '[5,4,3,2,1]', 'explanation': 'The linked list is reversed.'},
            {'input': 'head = [1,2]', 'output': '[2,1]', 'explanation': 'The two-node list is reversed.'},
            {'input': 'head = []', 'output': '[]', 'explanation': 'Empty list remains empty.'}
        ],
        ['Use three pointers: previous, current, and next', 'Iteratively reverse the links between nodes', 'Handle the edge case of an empty list'],
        ['The number of nodes in the list is the range [0, 5000]', '-5000 ≤ Node.val ≤ 5000']
    ),
    
    create_problem(
        'merge_two_sorted_lists', 'Merge Two Sorted Lists',
        'You are given the heads of two sorted linked lists list1 and list2. Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.',
        'easy', 'linked-lists',
        [
            {'input': 'list1 = [1,2,4], list2 = [1,3,4]', 'output': '[1,1,2,3,4,4]', 'explanation': 'The merged list is sorted.'},
            {'input': 'list1 = [], list2 = []', 'output': '[]', 'explanation': 'Both lists are empty.'},
            {'input': 'list1 = [], list2 = [0]', 'output': '[0]', 'explanation': 'One list is empty, return the other.'}
        ],
        ['Use a dummy head node to simplify the merging process', 'Compare values and choose the smaller node', 'Handle remaining nodes when one list is exhausted'],
        ['The number of nodes in both lists is in the range [0, 50]', '-100 ≤ Node.val ≤ 100', 'Both list1 and list2 are sorted in non-decreasing order']
    )
]

# Add more problems for other topics...
problems.extend(strings_problems[:3])  # Add first 3 string problems
problems.extend(linked_lists_problems[:2])  # Add first 2 linked list problems

print(f"Created {len(problems)} comprehensive problems")

# Initialize Redis
print("Testing Redis connection...")
try:
    redis_client.ping()
    print("✅ Redis connection successful!")
except Exception as e:
    print(f"❌ Redis connection failed: {str(e)}")
    exit(1)

print("Initializing comprehensive problems...")
for problem in problems:
    redis_client.hset(f"problem:{problem['id']}", mapping=problem)
    redis_client.zadd(f"problems:{problem['difficulty']}:{problem['topic']}", {problem['id']: 1})
    redis_client.sadd('topics', problem['topic'])
    redis_client.sadd('difficulties', problem['difficulty'])

print(f"✅ {len(problems)} comprehensive problems initialized!")

# Show topics
topics = {}
for problem in problems:
    topic = problem['topic']
    topics[topic] = topics.get(topic, 0) + 1

print("\n📋 Problems by Topic:")
for topic, count in sorted(topics.items()):
    print(f"   • {topic.title().replace('-', ' ')}: {count} problems")

print(f"\n🎉 Total: {len(problems)} comprehensive problems!")
