# LeetCode #394 - Decode String

**Data structure:** Stack  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/decode-string/

## Problem

Given an encoded string, return its decoded string. The encoding rule is `k[encoded_string]`, where the string inside the brackets is repeated exactly `k` times (`k` is a positive integer).

The input is always valid; digits appear only as repeat counts.

## Examples

```text
Input: s = "3[a]2[bc]"
Output: "aaabcbc"
```

```text
Input: s = "3[a2[c]]"
Output: "accaccacc"
```

```text
Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

## Constraints

- `1 <= s.length <= 30`
- `s` consists of lowercase letters, digits, and square brackets.
- All integers in `s` are in `[1, 300]`.
- Output length never exceeds `10^5`.

## Approach

Use a **stack** to remember the partial string and repeat count outside each pair of brackets, so nested patterns unwind correctly.

Scan character by character, keeping:

- `current` = the string being built at the current bracket depth
- `count` = the multiplier digits being read for the next bracket

Per character:

- **Digit** → accumulate `count = count * 10 + digit` (handles multi-digit `k`).
- **`[`** → entering a deeper level: push `(current, count)`, then reset `current = ""`, `count = 0`.
- **`]`** → finished an inner string: pop `(prev, k)` and set `current = prev + current * k`.
- **Letter** → append to `current`.

When the scan ends, `current` holds the decoded string. Each `[` saves the context to restore at its matching `]`, so arbitrary nesting works.

**Complexity**

- Time: `O(output length)`
- Space: `O(output length)`

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


class TestDecodeString(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.decodeString("3[a]2[bc]"), "aaabcbc")

    def test_example_2_nested(self):
        self.assertEqual(self.sol.decodeString("3[a2[c]]"), "accaccacc")

    def test_example_3_trailing(self):
        self.assertEqual(self.sol.decodeString("2[abc]3[cd]ef"), "abcabccdcdcdef")

    def test_multi_digit_count(self):
        self.assertEqual(self.sol.decodeString("10[a]"), "a" * 10)

    def test_deeply_nested(self):
        self.assertEqual(self.sol.decodeString("2[2[2[a]]]"), "a" * 8)

    def test_nested_with_prefix(self):
        self.assertEqual(self.sol.decodeString("3[a2[c]b]"), "accbaccbaccb")
```

## Interview tips

- The trick is pushing **both** the string-so-far and the multiplier on `[`, then combining on `]` — that's what makes nesting work.
- Build the multiplier with `count = count * 10 + digit` so multi-digit `k` (e.g. 10, 300) is handled — assuming single digits is a common bug.
- Reset `current` and `count` right after pushing, so the inner level starts clean.
- An alternative is recursion with an index pointer; same logic, but the explicit stack avoids recursion-depth concerns and is easy to explain.
- For very large outputs, push characters onto a list and `''.join` at the end instead of repeated concatenation.
