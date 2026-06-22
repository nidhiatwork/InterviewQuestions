# LeetCode #91 - Decode Ways

**Data structure:** String  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/decode-ways/

## Problem

A message of digits is decoded with the mapping `"1" -> 'A'`, …, `"26" -> 'Z'`. Digits must be grouped, then mapped back to letters — there may be many valid groupings.

For example `"11106"` decodes as `"AAJF"` (1 1 10 6) or `"KJF"` (11 10 6). The grouping `(1, 11, 06)` is invalid because `"06"` has a leading zero.

Given a digit string `s`, return the number of ways to decode it, or `0` if it cannot be decoded.

## Examples

```text
Input: s = "12"
Output: 2   ("AB" or "L")
```

```text
Input: s = "226"
Output: 3   ("BZ", "VF", "BBF")
```

```text
Input: s = "06"
Output: 0   (leading zero)
```

## Constraints

- `1 <= s.length <= 100`
- `s` contains only digits and may contain leading zero(s).

## Approach

Sweep the string left to right as a **state machine**, carrying just two rolling counts: the number of ways to decode the text ending at the previous position, and the number ending one position before that.

At each new digit, the ways to decode up to here depend on two local decisions:

- **Take the current digit alone** — valid only if it isn't `'0'`. Contributes "ways ending at the previous char".
- **Take the current digit with the previous one as a two-digit letter** — valid only if that pair is in `10..26`. Contributes "ways ending two chars back".

So we only need two rolling variables:

- `prev1` = ways to decode up to the previous character
- `prev2` = ways to decode up to the character before that

For each position: `cur = (single valid ? prev1 : 0) + (pair valid ? prev2 : 0)`, then slide: `prev2 = prev1`, `prev1 = cur`. Seed `prev2 = 1` (empty prefix) and `prev1 = 1` for a valid first char (or `0` if it's `'0'`).

This is the streaming form: constant memory, single pass, no table.

**Complexity**

- Time: `O(n)` — one pass
- Space: `O(1)` — two rolling counts

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


class TestNumDecodings(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.numDecodings("12"), 2)

    def test_example_2(self):
        self.assertEqual(self.sol.numDecodings("226"), 3)

    def test_leading_zero(self):
        self.assertEqual(self.sol.numDecodings("06"), 0)

    def test_two_seven_invalid_pair(self):
        self.assertEqual(self.sol.numDecodings("27"), 1)

    def test_hundred(self):
        self.assertEqual(self.sol.numDecodings("100"), 0)

    def test_all_ones(self):
        self.assertEqual(self.sol.numDecodings("111"), 3)
```

## Interview tips

- Frame it as a **streaming state machine** with two rolling counts; you never need a full array, only the last two running totals.
- The two transitions: single digit (valid if `!= '0'`) and two-digit pair (valid if `10..26`). Zeros are the trap — a `'0'` survives only as part of `10` or `20`.
- Seed `prev2 = 1` (empty prefix) so a valid leading two-digit pair is counted.
- Early-return `0` if `cur` ever becomes `0` — the string is undecodable (e.g. `"100"`, `"301"`).
- The recurrence is Fibonacci-shaped (`cur = prev1 + prev2` when both moves are valid), which is why all-ones strings grow like Fibonacci numbers.
