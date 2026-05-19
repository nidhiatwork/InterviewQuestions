"""LeetCode #150 — Evaluate Reverse Polish Notation  (Stack · Medium)

URL: https://leetcode.com/problems/evaluate-reverse-polish-notation/

Problem
-------
Evaluate an arithmetic expression in Reverse Polish Notation (postfix).
Valid operators: + - * / .  Each operand is an integer or another expression.
Integer division truncates TOWARD ZERO (not floor).

Examples
--------
  tokens = ["2","1","+","3","*"]                                        -> 9
  tokens = ["4","13","5","/","+"]                                       -> 6
  tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]    -> 22

Constraints
-----------
  1 <= tokens.length <= 10^4
  tokens[i] is an operator or an integer in [-200, 200].

Run
---
  python 2026-05-06-evaluate-reverse-polish-notation.py -v
"""

import unittest


class Solution:
    def evalRPN(self, tokens):
        raise NotImplementedError("Implement evalRPN")


# ----------------------------- tests -----------------------------

class TestEvalRPN(unittest.TestCase):
    def setUp(self):
        self.s = Solution()

    def test_example1_simple(self):
        self.assertEqual(self.s.evalRPN(["2", "1", "+", "3", "*"]), 9)

    def test_example2_with_division(self):
        self.assertEqual(self.s.evalRPN(["4", "13", "5", "/", "+"]), 6)

    def test_example3_complex_nested(self):
        tokens = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
        self.assertEqual(self.s.evalRPN(tokens), 22)

    def test_single_operand(self):
        self.assertEqual(self.s.evalRPN(["42"]), 42)

    def test_negative_operand(self):
        self.assertEqual(self.s.evalRPN(["-3"]), -3)

    def test_truncation_toward_zero_negative(self):
        # 6 / -4 truncated toward zero == -1 (NOT floor -2)
        self.assertEqual(self.s.evalRPN(["6", "-4", "/"]), -1)

    def test_truncation_toward_zero_positive(self):
        self.assertEqual(self.s.evalRPN(["7", "2", "/"]), 3)

    def test_subtraction_order(self):
        # 5 3 -  =>  5 - 3 == 2
        self.assertEqual(self.s.evalRPN(["5", "3", "-"]), 2)

    def test_division_order(self):
        # 20 4 /  =>  20 / 4 == 5
        self.assertEqual(self.s.evalRPN(["20", "4", "/"]), 5)

    def test_negative_intermediate_result(self):
        # 3 5 - 2 *  =>  (3 - 5) * 2 == -4
        self.assertEqual(self.s.evalRPN(["3", "5", "-", "2", "*"]), -4)

    def test_zero_token(self):
        self.assertEqual(self.s.evalRPN(["0", "5", "+"]), 5)

    def test_chained_subtraction(self):
        # 10 5 - 3 -  =>  (10 - 5) - 3 == 2
        self.assertEqual(self.s.evalRPN(["10", "5", "-", "3", "-"]), 2)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Textbook stack problem.
  - For each token: if it's a number push it; if it's an operator pop the top
    two operands (right first, then left), apply, push the result back.
  - After all tokens, the single stack entry is the answer.

Truncation gotcha
-----------------
Python's // floors toward negative infinity (-7 // 2 == -4), but the problem
requires truncation toward zero (-3). Use int(a / b) instead of a // b.

Complexity
----------
- Time:  O(n)
- Space: O(n)  (stack)

Python solution
---------------
class Solution:
    OPERATORS = {'+', '-', '*', '/'}

    def evalRPN(self, tokens):
        stack = []
        for token in tokens:
            if token in self.OPERATORS:
                right = stack.pop()
                left = stack.pop()
                stack.append(self._apply(token, left, right))
            else:
                stack.append(int(token))
        return stack[0]

    @staticmethod
    def _apply(op, a, b):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        return int(a / b)   # truncate toward zero, NOT floor

Interview tips
--------------
- State the truncation rule out loud — many candidates write a // b and miss
  the floor-vs-truncate difference for negatives.
- Pop order matters: right operand first, then left. Subtraction and division
  are non-commutative; verbally trace ["5","3","-"] to confirm 5 - 3 == 2.
- A small _apply helper or dict {op: fn} keeps the loop readable. Avoid eval()
  — interviewers mark it down for security and laziness.
- Mention `operator.add`, `operator.sub`, ... as the elegant variant even if
  you don't use it.
"""
