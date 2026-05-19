"""LeetCode #5 — Longest Palindromic Substring  (String · Medium)

URL: https://leetcode.com/problems/longest-palindromic-substring/

Problem
-------
Given a string `s`, return the longest palindromic substring in `s`.

Examples
--------
  s = "babad"  -> "bab"  ("aba" is also acceptable)
  s = "cbbd"   -> "bb"
  s = "a"      -> "a"

Constraints
-----------
  1 <= s.length <= 1000
  s consists of digits and English letters (case-sensitive).

Run
---
  python 2026-05-05-longest-palindromic-substring.py -v
"""

import unittest


class Solution:
    def longestPalindrome(self, s):
        raise NotImplementedError("Implement longestPalindrome")


# ----------------------------- tests -----------------------------

class TestLongestPalindrome(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_provided_babad(self):
        result = self.sol.longestPalindrome("babad")
        self.assertIn(result, {"bab", "aba"})

    def test_provided_cbbd(self):
        self.assertEqual(self.sol.longestPalindrome("cbbd"), "bb")

    def test_single_character(self):
        self.assertEqual(self.sol.longestPalindrome("a"), "a")

    def test_two_same_characters(self):
        self.assertEqual(self.sol.longestPalindrome("aa"), "aa")

    def test_two_different_characters(self):
        result = self.sol.longestPalindrome("ab")
        self.assertIn(result, {"a", "b"})

    def test_full_string_palindrome_odd(self):
        self.assertEqual(self.sol.longestPalindrome("racecar"), "racecar")

    def test_full_string_palindrome_even(self):
        self.assertEqual(self.sol.longestPalindrome("abba"), "abba")

    def test_no_repeating_characters(self):
        result = self.sol.longestPalindrome("abcdef")
        self.assertEqual(len(result), 1)
        self.assertIn(result, set("abcdef"))

    def test_palindrome_at_end(self):
        self.assertEqual(self.sol.longestPalindrome("xyzcbbc"), "cbbc")

    def test_palindrome_at_start(self):
        self.assertEqual(self.sol.longestPalindrome("abbaxyz"), "abba")

    def test_long_repeating(self):
        self.assertEqual(self.sol.longestPalindrome("aaaaaa"), "aaaaaa")

    def test_case_sensitive(self):
        result = self.sol.longestPalindrome("Aa")
        self.assertIn(result, {"A", "a"})


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Expand Around Center. Every palindrome has a center. For a string of length
n there are 2n - 1 possible centers — n for odd-length palindromes (a single
character) and n - 1 for even-length palindromes (between two adjacent chars).
For each center, expand outward while the two ends match. Keep the longest
palindromic substring seen.

The trick most candidates miss: handle the EVEN-length center.

Complexity
----------
- Time:  O(n^2)  (for each of 2n-1 centers, worst-case expansion is O(n))
- Space: O(1) auxiliary (excluding the output)

A O(n) Manacher's algorithm exists; mention only if asked.

Python solution
---------------
class Solution:
    def longestPalindrome(self, s):
        best = ''
        for i in range(len(s)):
            best = max(best, self._expand(s, i, i),     key=len)  # odd-length
            best = max(best, self._expand(s, i, i + 1), key=len)  # even-length
        return best

    def _expand(self, s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # The loop overshot by one step on each side, so the valid
        # palindrome is s[left+1 : right].
        return s[left + 1:right]

Why this shape over the index-juggling version
-----------------------------------------------
- _expand returns the actual palindrome substring, not an (l, r) index pair.
  No off-by-one bookkeeping leaks into the caller.
- max(best, ..., key=len) compares lengths directly — much more obvious than
  comparing `r1 - l1 > end - start`.
- Only ONE off-by-one to reason about: when the loop exits, both pointers
  have stepped one past the match, so the substring is s[left+1 : right].

Interview tips
--------------
- Lead with center-expansion (O(1) extra space), not DP (O(n^2) space).
- Don't forget the even-length center — that's the most common bug.
- State the overshoot reasoning out loud when explaining _expand.
- Bonus: mention Manacher's O(n) — signals depth even if you don't implement.
"""
