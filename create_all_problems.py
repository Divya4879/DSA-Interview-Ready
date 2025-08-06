#!/usr/bin/env python3
"""
Create all 80+ problems across 8 topics
"""

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
        'tags': json.dumps([topic.title()])
    }

# All 80+ problems across 8 topics
all_problems = []

# 1. ARRAYS (10 problems) - Already created above
# 2. STRINGS (10 problems)
strings_problems = [
    create_problem('valid_anagram', 'Valid Anagram', 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.', 'easy', 'strings',
        [{'input': 's = "anagram", t = "nagaram"', 'output': 'true', 'explanation': 'Both strings have same characters'},
         {'input': 's = "rat", t = "car"', 'output': 'false', 'explanation': 'Different characters'},
         {'input': 's = "a", t = "ab"', 'output': 'false', 'explanation': 'Different lengths'}],
        ['Count frequency of each character', 'Compare character frequencies', 'Or sort both strings and compare'],
        ['1 ≤ s.length, t.length ≤ 5 × 10⁴', 's and t consist of lowercase English letters']),
    
    create_problem('valid_palindrome', 'Valid Palindrome', 'A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.', 'easy', 'strings',
        [{'input': 's = "A man, a plan, a canal: Panama"', 'output': 'true', 'explanation': 'After processing: "amanaplanacanalpanama" is palindrome'},
         {'input': 's = "race a car"', 'output': 'false', 'explanation': 'After processing: "raceacar" is not palindrome'},
         {'input': 's = " "', 'output': 'true', 'explanation': 'Empty string after processing is palindrome'}],
        ['Use two pointers from both ends', 'Skip non-alphanumeric characters', 'Compare characters in lowercase'],
        ['1 ≤ s.length ≤ 2 × 10⁵', 's consists only of printable ASCII characters']),
    
    create_problem('longest_substring_no_repeat', 'Longest Substring Without Repeating Characters', 'Given a string s, find the length of the longest substring without repeating characters.', 'medium', 'strings',
        [{'input': 's = "abcabcbb"', 'output': '3', 'explanation': 'The answer is "abc", with the length of 3'},
         {'input': 's = "bbbbb"', 'output': '1', 'explanation': 'The answer is "b", with the length of 1'},
         {'input': 's = "pwwkew"', 'output': '3', 'explanation': 'The answer is "wke", with the length of 3'}],
        ['Use sliding window technique', 'Use hash set to track characters in current window', 'When duplicate found, move left pointer'],
        ['0 ≤ s.length ≤ 5 × 10⁴', 's consists of English letters, digits, symbols and spaces']),
    
    create_problem('group_anagrams', 'Group Anagrams', 'Given an array of strings strs, group the anagrams together.', 'medium', 'strings',
        [{'input': 'strs = ["eat","tea","tan","ate","nat","bat"]', 'output': '[["bat"],["nat","tan"],["ate","eat","tea"]]', 'explanation': 'Group strings that are anagrams'},
         {'input': 'strs = [""]', 'output': '[[""]]', 'explanation': 'Single empty string'},
         {'input': 'strs = ["a"]', 'output': '[["a"]]', 'explanation': 'Single character string'}],
        ['Sort each string to create a key', 'Use hash map with sorted string as key', 'Group strings with same sorted key'],
        ['1 ≤ strs.length ≤ 10⁴', '0 ≤ strs[i].length ≤ 100', 'strs[i] consists of lowercase English letters']),
    
    create_problem('valid_parentheses', 'Valid Parentheses', 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.', 'easy', 'strings',
        [{'input': 's = "()"', 'output': 'true', 'explanation': 'Valid pair of parentheses'},
         {'input': 's = "()[]{}"', 'output': 'true', 'explanation': 'All brackets properly matched'},
         {'input': 's = "(]"', 'output': 'false', 'explanation': 'Mismatched bracket types'}],
        ['Use a stack to track opening brackets', 'When closing bracket found, check if it matches top of stack', 'Stack should be empty at the end'],
        ['1 ≤ s.length ≤ 10⁴', 's consists of parentheses only \'()[]{}\'']),
    
    create_problem('longest_palindromic_substring', 'Longest Palindromic Substring', 'Given a string s, return the longest palindromic substring in s.', 'medium', 'strings',
        [{'input': 's = "babad"', 'output': '"bab"', 'explanation': '"aba" is also a valid answer'},
         {'input': 's = "cbbd"', 'output': '"bb"', 'explanation': 'Longest palindrome is "bb"'},
         {'input': 's = "a"', 'output': '"a"', 'explanation': 'Single character is palindrome'}],
        ['Expand around centers approach', 'Check both odd and even length palindromes', 'Keep track of longest palindrome found'],
        ['1 ≤ s.length ≤ 1000', 's consist of only digits and English letters']),
    
    create_problem('palindromic_substrings', 'Palindromic Substrings', 'Given a string s, return the number of palindromic substrings in it.', 'medium', 'strings',
        [{'input': 's = "abc"', 'output': '3', 'explanation': 'Three palindromic strings: "a", "b", "c"'},
         {'input': 's = "aaa"', 'output': '6', 'explanation': 'Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa"'},
         {'input': 's = "aba"', 'output': '4', 'explanation': 'Four palindromic strings: "a", "b", "a", "aba"'}],
        ['Expand around each possible center', 'Count palindromes of both odd and even lengths', 'Each single character is a palindrome'],
        ['1 ≤ s.length ≤ 1000', 's consists of lowercase English letters']),
    
    create_problem('encode_decode_strings', 'Encode and Decode Strings', 'Design an algorithm to encode a list of strings to a string and decode it back.', 'medium', 'strings',
        [{'input': 'input = ["lint","code","love","you"]', 'output': '"lint4#code4#love4#you"', 'explanation': 'Encode with length and delimiter'},
         {'input': 'input = ["we", "say", ":", "yes"]', 'output': '"we2#say3#:1#yes"', 'explanation': 'Handle special characters'},
         {'input': 'input = [""]', 'output': '"0#"', 'explanation': 'Empty string encoded'}],
        ['Use length prefix for each string', 'Add delimiter to separate strings', 'Parse length first when decoding'],
        ['0 ≤ strs.length < 200', '0 ≤ strs[i].length < 200', 'strs[i] contains any possible characters']),
    
    create_problem('minimum_window_substring', 'Minimum Window Substring', 'Given two strings s and t, return the minimum window substring of s such that every character in t is included in the window.', 'hard', 'strings',
        [{'input': 's = "ADOBECODEBANC", t = "ABC"', 'output': '"BANC"', 'explanation': 'Minimum window containing all characters of t'},
         {'input': 's = "a", t = "a"', 'output': '"a"', 'explanation': 'Entire string is the minimum window'},
         {'input': 's = "a", t = "aa"', 'output': '""', 'explanation': 'No valid window exists'}],
        ['Use sliding window with two pointers', 'Expand window until all characters of t are included', 'Contract window while maintaining validity'],
        ['m == s.length', 'n == t.length', '1 ≤ m, n ≤ 10⁵']),
    
    create_problem('character_replacement', 'Longest Repeating Character Replacement', 'You are given a string s and an integer k. You can choose any character and change it to any other character. Return the length of the longest substring containing the same letter you can get after performing at most k operations.', 'medium', 'strings',
        [{'input': 's = "ABAB", k = 2', 'output': '4', 'explanation': 'Replace the two \'A\'s with two \'B\'s or vice versa'},
         {'input': 's = "AABABBA", k = 1', 'output': '4', 'explanation': 'Replace one \'A\' in the middle to get "AABBBBA"'},
         {'input': 's = "ABCDE", k = 1', 'output': '2', 'explanation': 'Replace any character to get length 2'}],
        ['Use sliding window technique', 'Track frequency of characters in current window', 'Window is valid if (window_size - max_frequency) <= k'],
        ['1 ≤ s.length ≤ 10⁵', 's consists of only uppercase English letters', '0 ≤ k ≤ s.length'])
]

all_problems.extend(strings_problems)

print(f"Generated {len(all_problems)} problems so far...")
print("This script shows the pattern - need to add 6 more topics to reach 80+ problems")

# Show what we have so far
topics = {}
for problem in all_problems:
    topic = problem['topic']
    if topic not in topics:
        topics[topic] = 0
    topics[topic] += 1

print("\nTopics created so far:")
for topic, count in topics.items():
    print(f"   • {topic.title()}: {count} problems")

print(f"\nTotal: {len(all_problems)} problems")
print("Need to add: linked-lists, trees, graphs, dynamic-programming, stacks, heaps (6 more topics)")
