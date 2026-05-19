"""LeetCode #49 — Group Anagrams  (Hash Table · Medium)

URL: https://leetcode.com/problems/group-anagrams/

Problem
-------
Given an array of strings `strs`, group the anagrams together. You can return
the answer in any order.

Examples
--------
  strs = ["eat","tea","tan","ate","nat","bat"]
    -> [["bat"],["nat","tan"],["ate","eat","tea"]]
  strs = [""]   -> [[""]]
  strs = ["a"]  -> [["a"]]

Constraints
-----------
  1 <= strs.length <= 10^4
  0 <= strs[i].length <= 100
  strs[i] consists of lowercase English letters only.

Run
---
  python 2026-05-04-group-anagrams.py -v
"""

from collections import Counter
import unittest


class Solution:
    def groupAnagrams(self, strs):
        raise NotImplementedError("Implement groupAnagrams")


# ----------------------------- tests -----------------------------

class TestGroupAnagrams(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    @staticmethod
    def _normalize(groups):
        return {frozenset(g) for g in groups}

    def test_example_1_basic(self):
        out = self.sol.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        self.assertEqual(self._normalize(out), self._normalize(expected))

    def test_example_2_single_empty_string(self):
        self.assertEqual(self.sol.groupAnagrams([""]), [[""]])

    def test_example_3_single_char(self):
        self.assertEqual(self.sol.groupAnagrams(["a"]), [["a"]])

    def test_all_same_anagram(self):
        out = self.sol.groupAnagrams(["abc", "bca", "cab", "bac"])
        self.assertEqual(len(out), 1)
        self.assertEqual(set(out[0]), {"abc", "bca", "cab", "bac"})

    def test_no_anagrams(self):
        out = self.sol.groupAnagrams(["abc", "def", "ghi"])
        self.assertEqual(len(out), 3)
        self.assertEqual(
            self._normalize(out),
            {frozenset(["abc"]), frozenset(["def"]), frozenset(["ghi"])},
        )

    def test_duplicates_preserved(self):
        out = self.sol.groupAnagrams(["eat", "eat", "tea"])
        self.assertEqual(len(out), 1)
        self.assertEqual(Counter(out[0]), Counter(["eat", "eat", "tea"]))

    def test_large_input_stress(self):
        strs = ["abcde"] * 5000 + ["edcba"] * 2500 + ["bcdea"] * 2500
        out = self.sol.groupAnagrams(strs)
        self.assertEqual(len(out), 1)
        self.assertEqual(len(out[0]), 10000)

    def test_mixed_lengths(self):
        out = self.sol.groupAnagrams(["a", "aa", "aaa", "a"])
        self.assertEqual(
            self._normalize(out),
            {frozenset(["a", "a"]), frozenset(["aa"]), frozenset(["aaa"])},
        )


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Two strings are anagrams iff they have the same character counts. Build a
canonical key per string and group by that key in a hash map.

Two natural keys:
  1. Sorted string: ''.join(sorted(s))                     -> O(N * K log K)
  2. 26-tuple of letter counts (chosen here)               -> O(N * K)

Lists are unhashable; convert the count array to a tuple for the dict key.

Complexity
----------
- Time:  O(N * K) where N = number of strings, K = max string length
- Space: O(N * K)

Python solution
---------------
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        groups = defaultdict(list)
        for s in strs:
            key = [0] * 26
            for ch in s:
                key[ord(ch) - ord('a')] += 1
            groups[tuple(key)].append(s)
        return list(groups.values())

Interview tips
--------------
- Lead with the insight ("same character counts"), not the code.
- Compare the sort vs count-tuple tradeoff out loud; pick count-tuple because
  K log K -> K is the asymptotic win.
- Watch the empty-string edge case: groupAnagrams([""]) must return [[""]],
  not []. Many naive solutions silently mishandle this.
- Mention the tuple-key trick: lists are unhashable in Python because they're
  mutable; tuple() gives an immutable, hashable key.
"""
