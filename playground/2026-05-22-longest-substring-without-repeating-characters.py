"""LeetCode #3 — Longest Substring Without Repeating Characters  (String · Medium)

URL: https://leetcode.com/problems/longest-substring-without-repeating-characters/

Problem
-------
Given a string `s`, find the length of the longest substring without
duplicate characters.

Examples
--------
  s = "abcabcbb"  -> 3   ("abc")
  s = "bbbbb"     -> 1   ("b")
  s = "pwwkew"    -> 3   ("wke"; note "pwke" is a SUBSEQUENCE, not a substring)

Constraints
-----------
  0 <= s.length <= 5 * 10^4
  s consists of English letters, digits, symbols and spaces.

Run
---
  python 2026-05-22-longest-substring-without-repeating-characters.py -v
"""

import unittest


class Solution:
    def lengthOfLongestSubstring(self, s):
        raise NotImplementedError("Implement lengthOfLongestSubstring")


# ----------------------------- tests -----------------------------

class TestLengthOfLongestSubstring(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_provided_abcabcbb(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("abcabcbb"), 3)

    def test_provided_bbbbb(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("bbbbb"), 1)

    def test_provided_pwwkew(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("pwwkew"), 3)

    def test_empty_string(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring(""), 0)

    def test_single_character(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("a"), 1)

    def test_all_unique(self):
        self.assertEqual(self.sol.lengthOfLongestSubstring("abcdef"), 6)

    def test_repeat_at_end(self):
        # "dvdf" -> "vdf" of length 3
        self.assertEqual(self.sol.lengthOfLongestSubstring("dvdf"), 3)

    def test_repeat_far_apart(self):
        # "abba" — left pointer must NOT jump back. Answer = "ab" or "ba" = 2.
        self.assertEqual(self.sol.lengthOfLongestSubstring("abba"), 2)

    def test_spaces_and_symbols(self):
        # "  " has length 2 but only one distinct char, so answer is 1.
        self.assertEqual(self.sol.lengthOfLongestSubstring("  "), 1)
        # Mixed digits, letters, symbols all unique.
        self.assertEqual(self.sol.lengthOfLongestSubstring("a1!b2@"), 6)

    def test_case_sensitive(self):
        # Upper- and lower-case are distinct.
        self.assertEqual(self.sol.lengthOfLongestSubstring("aA"), 2)

    def test_long_window_at_start(self):
        # "tmmzuxt" -> longest is "mzuxt" of length 5.
        self.assertEqual(self.sol.lengthOfLongestSubstring("tmmzuxt"), 5)

    def test_large_alternating(self):
        # 10000 chars alternating 'a','b' -> longest unique window is just 2.
        self.assertEqual(self.sol.lengthOfLongestSubstring("ab" * 5000), 2)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Sliding window with a hash map of `char -> last index seen`.

Maintain two pointers, `left` and `right`, defining the current window
`s[left..right]` that contains no duplicates. Scan `right` from 0 to n-1:

1. If `s[right]` was seen at index `j` AND `j >= left`, then the duplicate
   is INSIDE the current window — jump `left` to `j + 1` to evict it.
2. Otherwise the duplicate (if any) is to the left of the window, so leave
   `left` alone.
3. Record `s[right] -> right` in the map.
4. Update `best = max(best, right - left + 1)`.

The critical pitfall is step 1's `j >= left` guard. Without it, "abba"
incorrectly shrinks the window when scanning the second 'a' (whose last
index is 0, which lies BEFORE the current left=2). Forgetting this guard
silently breaks the "tmmzuxt" and "abba" cases — both are favourite
interviewer traps.

Complexity
----------
- Time:  O(n)   — each index is visited once by `right` and at most once by `left`.
- Space: O(min(n, sigma)) — sigma = alphabet size (constant for ASCII).

Python solution
---------------
class Solution:
    def lengthOfLongestSubstring(self, s):
        last_seen = {}
        left = 0
        best = 0
        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1
            last_seen[ch] = right
            best = max(best, right - left + 1)
        return best

Why this shape over the "set + while pop" version
--------------------------------------------------
- Index-map version is O(n) with a single pass — `left` jumps in O(1).
- The set-based version (add `s[right]` into a set, while duplicate pop
  `s[left]` and advance `left`) is also O(n) amortised but does more work
  on repeated runs. Both are correct; the index-map is the one Microsoft
  interviewers prefer because the jump is explicit.
- Don't shadow Python's `set` or `str`; use clear names like `last_seen`.

Interview tips
--------------
- Lead with "sliding window with a last-seen index map" — that one sentence
  signals you know the optimal pattern.
- The `j >= left` guard is the #1 thing interviewers probe. Say it OUT LOUD:
  "I only shrink the window when the previous occurrence is INSIDE it."
- Walk through "abba" on a whiteboard to prove your guard works.
- State complexity early — both time and space, with the alphabet-size
  caveat. It signals depth.
- Edge cases: empty string, single char, all-unique, all-same, very long
  alternating pattern (window never grows past 2). Cover these in tests.
- Mention follow-ups: (a) "longest substring with at most k distinct chars"
  (LC 340) and (b) "minimum window substring" (LC 76) — they reuse this
  template and showing awareness is a strong signal.
"""
