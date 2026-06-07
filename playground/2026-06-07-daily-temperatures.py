"""
LeetCode #739 - Daily Temperatures  (Stack - Medium)
URL: https://leetcode.com/problems/daily-temperatures/

Problem
-------
Given an array of integers temperatures representing the daily temperatures,
return an array answer such that answer[i] is the number of days you have to
wait after the ith day to get a warmer temperature.

If there is no future day for which this is possible, keep answer[i] == 0.

Examples
--------
1) Input:  temperatures = [73,74,75,71,69,72,76,73]
   Output: [1,1,4,2,1,1,0,0]

2) Input:  temperatures = [30,40,50,60]
   Output: [1,1,1,0]

3) Input:  temperatures = [30,60,90]
   Output: [1,1,0]

Constraints
-----------
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100

Run
---
    python 2026-06-07-daily-temperatures.py -v
"""

import unittest


class Solution:
    def dailyTemperatures(self, temperatures):
        raise NotImplementedError("Implement dailyTemperatures")


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

    def test_short_increasing(self):
        self.assertEqual(self.sol.dailyTemperatures([30, 60, 90]), [1, 1, 0])

    def test_strictly_decreasing(self):
        self.assertEqual(self.sol.dailyTemperatures([90, 80, 70, 60]), [0, 0, 0, 0])

    def test_all_same_temperature(self):
        self.assertEqual(self.sol.dailyTemperatures([70, 70, 70]), [0, 0, 0])

    def test_single_day(self):
        self.assertEqual(self.sol.dailyTemperatures([55]), [0])

    def test_late_warmer_day(self):
        self.assertEqual(self.sol.dailyTemperatures([60, 50, 40, 70]), [3, 2, 1, 0])

    def test_duplicate_temperatures_then_warmer(self):
        self.assertEqual(self.sol.dailyTemperatures([65, 65, 66, 64, 67]), [2, 1, 2, 1, 0])

    def test_warmer_for_some_not_all(self):
        self.assertEqual(self.sol.dailyTemperatures([80, 70, 75, 71, 72]), [0, 1, 0, 1, 0])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Use a stack of indexes whose warmer day has not been found yet. Keep the stack
monotonically decreasing by temperature:

1. Scan days from left to right.
2. For the current temperature, pop previous indexes while the current day is
   warmer than the temperature at the top index.
3. For each popped index `j`, the answer is `i - j` because day `i` is the first
   warmer day after `j`.
4. Push the current index because it may need a warmer future day.

Why the stack works: an index stays on the stack only while every day seen after
it has been less than or equal to its temperature. The first warmer day that
breaks that condition resolves it immediately.

Complexity
----------
- Time:  O(n), because each index is pushed once and popped at most once.
- Space: O(n), for the unresolved-index stack.

Python solution
---------------
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

Interview tips
--------------
- Say "monotonic stack of indexes", not values, because the answer needs distances.
- Equal temperatures do not count as warmer, so the while condition is `>`, not `>=`.
- Unresolved indexes naturally remain 0 in the answer array.
- Explain amortized O(n): every index is pushed once and popped once.
- If asked for a right-to-left version, keep candidate warmer days on the stack and
  pop days that are not warmer than the current day.
"""
