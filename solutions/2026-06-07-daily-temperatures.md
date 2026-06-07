# LeetCode #739 - Daily Temperatures

**Data structure:** Stack  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/daily-temperatures/

## Problem

Given an array of integers `temperatures` representing the daily temperatures, return an array `answer` where `answer[i]` is the number of days you must wait after day `i` to get a warmer temperature.

If there is no future warmer day, `answer[i]` should be `0`.

## Examples

```text
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

```text
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]
```

```text
Input: temperatures = [30,60,90]
Output: [1,1,0]
```

## Constraints

- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`

## Approach

Use a stack of indexes whose next warmer day has not been found yet.

Scan from left to right:

1. Keep indexes on the stack in decreasing temperature order.
2. When the current temperature is warmer than the temperature at the top stack index, pop that old index.
3. The current day is the first warmer day for the popped index, so fill `answer[old] = current - old`.
4. Push the current index for future days to resolve.

The stack stores indexes, not temperatures, because the answer asks for a distance in days.

**Complexity**

- Time: `O(n)` because each index is pushed once and popped at most once
- Space: `O(n)` for the stack

## Python solution

```python
class Solution:
    def dailyTemperatures(self, temperatures):
        answer = [0] * len(temperatures)
        stack = []

        for i, temp in enumerate(temperatures):
            while stack and temp > temperatures[stack[-1]]:
                prev = stack.pop()
                answer[prev] = i - prev
            stack.append(i)

        return answer
```

## unittest test cases

```python
import unittest


class TestDailyTemperatures(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_mixed_temperatures(self):
        self.assertEqual(
            self.sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]),
            [1, 1, 4, 2, 1, 1, 0, 0],
        )

    def test_strictly_increasing(self):
        self.assertEqual(self.sol.dailyTemperatures([30, 40, 50, 60]), [1, 1, 1, 0])

    def test_strictly_decreasing(self):
        self.assertEqual(self.sol.dailyTemperatures([90, 80, 70, 60]), [0, 0, 0, 0])

    def test_all_same_temperature(self):
        self.assertEqual(self.sol.dailyTemperatures([70, 70, 70]), [0, 0, 0])

    def test_late_warmer_day(self):
        self.assertEqual(self.sol.dailyTemperatures([60, 50, 40, 70]), [3, 2, 1, 0])
```

## Interview tips

- Use the phrase "monotonic stack of indexes."
- Equal temperatures are not warmer, so use `>` instead of `>=`.
- Leave unresolved days as `0`; no cleanup pass is needed.
- Explain the amortized cost: each index is pushed once and popped once.
- If the interviewer asks for a right-to-left variant, pop any candidate day whose temperature is less than or equal to the current temperature.
