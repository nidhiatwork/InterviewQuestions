"""
LeetCode #91 - Decode Ways  (String - Medium)
URL: https://leetcode.com/problems/decode-ways/

Problem
-------
You have intercepted a secret message encoded as a string of numbers. The message
is decoded via the following mapping:

    "1" -> 'A'
    "2" -> 'B'
    ...
    "25" -> 'Y'
    "26" -> 'Z'

To decode a message, all the digits must be grouped, then mapped back into
letters using the reverse of the mapping above (there may be many ways). For
example, "11106" can be decoded into:

    - "AAJF" with the grouping (1, 1, 10, 6)
    - "KJF"  with the grouping (11, 10, 6)

Note that the grouping (1, 11, 06) is invalid because "06" cannot be mapped into
'F' since "6" is different from "06".

Given a string s containing only digits, return the number of ways to decode it.
If the entire string cannot be decoded in any valid way, return 0.

The test cases are generated so that the answer fits in a 32-bit integer.

Examples
--------
1) Input:  s = "12"
   Output: 2
   Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

2) Input:  s = "226"
   Output: 3
   Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or
   "BBF" (2 2 6).

3) Input:  s = "06"
   Output: 0
   Explanation: "06" cannot be mapped to "F" because of the leading zero ("6" is
   different from "06").

Constraints
-----------
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s).

Run
---
    python 2026-06-22-decode-ways.py -v
"""

import unittest


class Solution:
    def numDecodings(self, s):
        raise NotImplementedError("Implement numDecodings")


class TestNumDecodings(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.numDecodings("12"), 2)

    def test_example_2(self):
        self.assertEqual(self.sol.numDecodings("226"), 3)

    def test_leading_zero(self):
        self.assertEqual(self.sol.numDecodings("06"), 0)

    def test_single_digit(self):
        self.assertEqual(self.sol.numDecodings("8"), 1)

    def test_single_zero(self):
        self.assertEqual(self.sol.numDecodings("0"), 0)

    def test_two_six_valid_pair(self):
        self.assertEqual(self.sol.numDecodings("26"), 2)

    def test_two_seven_invalid_pair(self):
        # 27 cannot be a single letter (>26), only 2 7
        self.assertEqual(self.sol.numDecodings("27"), 1)

    def test_ten(self):
        self.assertEqual(self.sol.numDecodings("10"), 1)

    def test_hundred(self):
        # "100": 1 00 invalid, 10 0 invalid -> 0
        self.assertEqual(self.sol.numDecodings("100"), 0)

    def test_long_ones(self):
        # "11106" -> (1 1 10 6) and (11 10 6) = 2
        self.assertEqual(self.sol.numDecodings("11106"), 2)

    def test_all_ones(self):
        # "111" -> 1 1 1 / 11 1 / 1 11 = 3 (Fibonacci-like)
        self.assertEqual(self.sol.numDecodings("111"), 3)

    def test_trailing_zero_invalid(self):
        self.assertEqual(self.sol.numDecodings("301"), 0)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Sweep the string left to right as a state machine, carrying just two rolling
counts: the number of ways to decode the text ending at the previous position,
and the number ending one position before that.

At each new digit, the number of ways to decode up to here depends only on two
local decisions:
  - Take the current digit ALONE. Valid only if it is not '0'. If valid, it
    contributes "ways ending at the previous char" to the running total.
  - Take the current digit together with the previous digit as a two-digit
    letter. Valid only if that pair is between 10 and 26 inclusive. If valid, it
    contributes "ways ending two chars back" to the running total.

So we only ever need two rolling variables:
  - prev1 = ways to decode the string up to the previous character
  - prev2 = ways to decode the string up to the character before that

For each position compute cur = (single-digit valid ? prev1 : 0) +
(two-digit valid ? prev2 : 0), then slide the window: prev2 = prev1, prev1 = cur.

Seed: prev2 = 1 (one way to decode the empty prefix), prev1 = 1 for a valid
first character or 0 if the first character is '0'.

This is the streaming form: constant memory, single pass, no table.

Complexity
----------
- Time:  O(n), one pass over the string.
- Space: O(1), just two rolling counts.

Python solution
---------------
class Solution:
    def numDecodings(self, s):
        if not s or s[0] == '0':
            return 0

        prev2 = 1            # ways to decode empty prefix
        prev1 = 1            # ways to decode s[0] (valid, since s[0] != '0')

        for i in range(1, len(s)):
            cur = 0
            if s[i] != '0':                       # current digit stands alone
                cur += prev1
            two = int(s[i - 1:i + 1])             # current + previous as a pair
            if 10 <= two <= 26:                   # valid two-digit letter
                cur += prev2
            if cur == 0:                          # dead end, nothing decodes
                return 0
            prev2, prev1 = prev1, cur

        return prev1

Interview tips
--------------
- Frame it as a streaming state machine with two rolling counts; you never need
  a full array, only the last two running totals.
- The two transitions are: single digit (valid if != '0') and two-digit pair
  (valid if 10..26). Zeros are the trap: '0' can only survive as part of 10 or 20.
- Seed prev2 = 1 (empty prefix) so a valid leading two-digit pair is counted.
- Early-return 0 if at any point cur becomes 0 - the string is undecodable (e.g.
  "100", "301").
- The recurrence is Fibonacci-shaped (cur = prev1 + prev2 when both moves are
  valid), which is why all-ones strings grow like Fibonacci numbers.
"""
