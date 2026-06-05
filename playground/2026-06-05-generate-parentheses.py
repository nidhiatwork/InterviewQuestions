"""
LeetCode #22 - Generate Parentheses  (String · Medium)
URL: https://leetcode.com/problems/generate-parentheses/

Problem
-------
Given n pairs of parentheses, write a function to generate all combinations of
well-formed parentheses.

Examples
--------
1) Input:  n = 3
   Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

2) Input:  n = 1
   Output: ["()"]

3) Input:  n = 2
   Output: ["(())", "()()"]

Constraints
-----------
- 1 <= n <= 8

Run
---
    python 2026-06-05-generate-parentheses.py -v
"""

import unittest


class Solution:
    def generateParenthesis(self, n):
        raise NotImplementedError("Implement generateParenthesis")


class TestGenerateParentheses(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertParenthesesEqual(self, actual, expected):
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), len(expected))

    def test_example_n_3(self):
        expected = ["((()))", "(()())", "(())()", "()(())", "()()()"]
        self.assertParenthesesEqual(self.sol.generateParenthesis(3), expected)

    def test_example_n_1(self):
        self.assertEqual(self.sol.generateParenthesis(1), ["()"])

    def test_n_2(self):
        self.assertParenthesesEqual(self.sol.generateParenthesis(2), ["(())", "()()"])

    def test_n_4_count_and_validity(self):
        result = self.sol.generateParenthesis(4)
        self.assertEqual(len(result), 14)
        for item in result:
            self.assertTrue(is_valid_parentheses(item))

    def test_no_duplicates(self):
        result = self.sol.generateParenthesis(5)
        self.assertEqual(len(result), len(set(result)))

    def test_each_string_has_correct_length(self):
        for n in range(1, 6):
            for item in self.sol.generateParenthesis(n):
                self.assertEqual(len(item), 2 * n)

    def test_all_results_are_balanced_prefixes(self):
        for item in self.sol.generateParenthesis(4):
            balance = 0
            for ch in item:
                balance += 1 if ch == "(" else -1
                self.assertGreaterEqual(balance, 0)
            self.assertEqual(balance, 0)


def is_valid_parentheses(s):
    balance = 0
    for ch in s:
        balance += 1 if ch == "(" else -1
        if balance < 0:
            return False
    return balance == 0


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Build each answer from left to right while tracking how many open and close
parentheses have already been used.

At any position:

1. You may add "(" if fewer than n opens have been used.
2. You may add ")" only if it would not make the prefix invalid, meaning the
   number of closes used is still less than the number of opens used.
3. Once the string reaches length 2 * n, record it.

This works because every partial string is kept valid as it is built, so there
is no need to generate bad strings and filter them afterward.

Complexity
----------
- Time:  O(Cn * n), where Cn is the nth Catalan number. There are Cn valid
         strings and copying each finished string costs O(n).
- Space: O(n) recursion depth, excluding the output list.

Python solution
---------------
class Solution:
    def generateParenthesis(self, n):
        result = []
        path = []

        def build(open_used, close_used):
            if len(path) == 2 * n:
                result.append("".join(path))
                return

            if open_used < n:
                path.append("(")
                build(open_used + 1, close_used)
                path.pop()

            if close_used < open_used:
                path.append(")")
                build(open_used, close_used + 1)
                path.pop()

        build(0, 0)
        return result

Interview tips
--------------
- The core invariant is: never let closes exceed opens in any prefix.
- Explain why this avoids invalid candidates instead of filtering them later.
- For n = 3, draw the decision tree for the first few levels if the interviewer
  wants intuition.
- Order usually does not matter unless the problem explicitly asks for it, but
  this approach naturally produces the common LeetCode order.
- If asked about count, mention that the number of answers follows the Catalan
  sequence.
"""
