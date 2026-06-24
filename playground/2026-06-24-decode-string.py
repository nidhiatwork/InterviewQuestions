"""
LeetCode #394 - Decode String  (Stack - Medium)
URL: https://leetcode.com/problems/decode-string/

Problem
-------
Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the
square brackets is being repeated exactly k times. Note that k is guaranteed to
be a positive integer.

You may assume that the input string is always valid; there are no extra white
spaces, square brackets are well-formed, etc. Furthermore, you may assume that
the original data does not contain any digits and that digits are only for those
repeat numbers, k. For example, there will not be input like 3a or 2[4].

The test cases are generated so that the length of the output will never exceed
10^5.

Examples
--------
1) Input:  s = "3[a]2[bc]"
   Output: "aaabcbc"

2) Input:  s = "3[a2[c]]"
   Output: "accaccacc"

3) Input:  s = "2[abc]3[cd]ef"
   Output: "abcabccdcdcdef"

Constraints
-----------
- 1 <= s.length <= 30
- s consists of lowercase English letters, digits, and square brackets '[]'.
- s is guaranteed to be a valid input.
- All the integers in s are in the range [1, 300].

Run
---
    python 2026-06-24-decode-string.py -v
"""

import unittest


class Solution:
    def decodeString(self, s):
        raise NotImplementedError("Implement decodeString")


class TestDecodeString(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.decodeString("3[a]2[bc]"), "aaabcbc")

    def test_example_2_nested(self):
        self.assertEqual(self.sol.decodeString("3[a2[c]]"), "accaccacc")

    def test_example_3_trailing(self):
        self.assertEqual(self.sol.decodeString("2[abc]3[cd]ef"), "abcabccdcdcdef")

    def test_no_encoding(self):
        self.assertEqual(self.sol.decodeString("abcd"), "abcd")

    def test_single_repeat(self):
        self.assertEqual(self.sol.decodeString("1[x]"), "x")

    def test_multi_digit_count(self):
        self.assertEqual(self.sol.decodeString("10[a]"), "a" * 10)

    def test_deeply_nested(self):
        self.assertEqual(self.sol.decodeString("2[2[2[a]]]"), "a" * 8)

    def test_leading_letters_then_encode(self):
        self.assertEqual(self.sol.decodeString("abc3[d]"), "abcddd")

    def test_nested_with_prefix(self):
        self.assertEqual(self.sol.decodeString("3[a2[c]b]"), "accbaccbaccb")


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Use a stack to remember the partial string and repeat count outside each pair of
brackets, so nested patterns unwind correctly.

Scan the string character by character and keep:
  - `current` = the string being built at the CURRENT bracket depth
  - `count`   = the multiplier digits being read for the NEXT bracket

Rules per character:
  - Digit: accumulate it into `count` (count = count * 10 + digit), so multi-digit
    numbers like 10 work.
  - '[' : we are entering a deeper level. Push (current, count) onto the stack,
    then reset current = "" and count = 0 to start the inner string fresh.
  - ']' : we finished an inner string. Pop (prev_string, k); the decoded piece is
    prev_string + current * k. Set current to that.
  - Letter: append it to `current`.

When the scan ends, `current` holds the fully decoded string. The stack handles
arbitrary nesting because each '[' saves the context to restore at the matching
']'.

Complexity
----------
- Time:  O(output length), each output character is produced once.
- Space: O(output length) for the stack and the building strings.

Python solution
---------------
class Solution:
    def decodeString(self, s):
        stack = []            # holds (string_so_far, repeat_count)
        current = ""
        count = 0

        for ch in s:
            if ch.isdigit():
                count = count * 10 + int(ch)
            elif ch == '[':
                stack.append((current, count))
                current = ""
                count = 0
            elif ch == ']':
                prev, k = stack.pop()
                current = prev + current * k
            else:
                current += ch

        return current

Interview tips
--------------
- The trick is pushing BOTH the string-so-far and the multiplier on '[', then
  combining on ']'. That is what makes nesting work.
- Build the multiplier with count = count*10 + digit so multi-digit k (e.g. 10,
  300) is handled - a common bug is assuming single digits.
- Reset current and count to empty/0 right after pushing, so the inner level
  starts clean.
- An alternative is recursion with an index pointer; it mirrors the same logic
  but the explicit stack avoids recursion-depth concerns and is easy to explain.
- Repeatedly concatenating strings is fine here given small constraints; for huge
  outputs you could push characters onto a list and ''.join at the end.
"""
