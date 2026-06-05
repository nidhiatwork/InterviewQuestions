# LeetCode #22 - Generate Parentheses

**Data structure:** String  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/generate-parentheses/

## Problem

Given `n` pairs of parentheses, generate all combinations of well-formed parentheses.

## Examples

```text
Input: n = 3
Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]
```

```text
Input: n = 1
Output: ["()"]
```

```text
Input: n = 2
Output: ["(())", "()()"]
```

## Constraints

- `1 <= n <= 8`

## Approach

Build the string one character at a time while tracking how many opening and closing parentheses have already been used.

At each step:

1. Add `(` if we still have opening parentheses left.
2. Add `)` only when doing so keeps the prefix valid, meaning `close_used < open_used`.
3. When the string length reaches `2 * n`, add it to the answer.

The key invariant is that no prefix is ever invalid. That means we only build valid candidates and never need a cleanup/filter pass at the end.

**Complexity**

- Time: `O(Cn * n)`, where `Cn` is the nth Catalan number
- Space: `O(n)` call depth, excluding the output

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


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
```

## Interview tips

- Lead with the invariant: a valid prefix can never have more `)` than `(`.
- Mention that this generates only valid strings instead of generating all strings and filtering.
- Use `path.append(...)`, recurse, then `path.pop()` to keep string building efficient.
- The output size is Catalan-number sized, so exponential-looking growth is expected.
- If the interviewer asks for lexicographic-style order, try `(` before `)`, as shown above.
