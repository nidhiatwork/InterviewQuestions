"""LeetCode #198 — House Robber  (Dynamic Programming · Medium)

URL: https://leetcode.com/problems/house-robber/

Problem
-------
You are a professional robber planning to rob houses along a street. Each
house has a certain amount of money stashed. The only constraint stopping
you from robbing each of them is that adjacent houses have security systems
connected, and it will automatically contact the police if two adjacent
houses were broken into on the same night.

Given an integer array `nums` representing the amount of money of each house,
return the maximum amount of money you can rob tonight WITHOUT alerting the
police.

Examples
--------
  nums = [1,2,3,1]      -> 4    (rob houses 0 and 2: 1 + 3 = 4)
  nums = [2,7,9,3,1]    -> 12   (rob houses 0, 2, 4: 2 + 9 + 1 = 12)
  nums = [2,1,1,2]      -> 4    (rob houses 0 and 3: 2 + 2 = 4)

Constraints
-----------
  1 <= nums.length <= 100
  0 <= nums[i] <= 400

Run
---
  python 2026-05-18-house-robber.py -v
"""

import unittest


class Solution:
    def rob(self, nums):
        raise NotImplementedError("Implement rob")


# ----------------------------- tests -----------------------------

class TestHouseRobber(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.rob([1, 2, 3, 1]), 4)

    def test_example_2(self):
        self.assertEqual(self.sol.rob([2, 7, 9, 3, 1]), 12)

    def test_example_3_non_obvious(self):
        # Greedy would pick house 1 (value 7) but optimal skips it.
        self.assertEqual(self.sol.rob([2, 1, 1, 2]), 4)

    def test_single_house(self):
        self.assertEqual(self.sol.rob([5]), 5)

    def test_single_house_zero(self):
        self.assertEqual(self.sol.rob([0]), 0)

    def test_two_houses_pick_max(self):
        # Adjacent => can only pick one.
        self.assertEqual(self.sol.rob([2, 7]), 7)
        self.assertEqual(self.sol.rob([7, 2]), 7)
        self.assertEqual(self.sol.rob([5, 5]), 5)

    def test_three_houses_skip_middle(self):
        # Optimal: rob ends, skip middle: 5 + 5 = 10.
        self.assertEqual(self.sol.rob([5, 1, 5]), 10)

    def test_all_zeros(self):
        self.assertEqual(self.sol.rob([0, 0, 0, 0]), 0)

    def test_increasing_sequence(self):
        # 1 + 3 + 5 = 9 vs 2 + 4 = 6 -> pick odd indices? No: 0,2,4 = 1+3+5=9
        self.assertEqual(self.sol.rob([1, 2, 3, 4, 5]), 9)

    def test_large_constant(self):
        # All houses have 400; pick every other one. n=100 -> 50 * 400 = 20000.
        self.assertEqual(self.sol.rob([400] * 100), 20000)

    def test_alternating_high_low(self):
        # High houses are at even indices; rob all of them.
        self.assertEqual(self.sol.rob([100, 1, 100, 1, 100]), 300)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
At each house you make ONE decision: rob it or skip it.
  - If you rob house i, you get nums[i] + best(everything up to i-2).
  - If you skip house i, you carry forward best(everything up to i-1).
Take the max.

Recurrence
----------
  dp[i] = max( dp[i-1],            # skip house i
               dp[i-2] + nums[i] ) # rob house i

Base cases:
  dp[0] = nums[0]
  dp[1] = max(nums[0], nums[1])

Space optimization
------------------
You only ever look back TWO steps. Replace the dp array with two rolling
variables:
  prev2 = best up to i-2
  prev1 = best up to i-1
At step i: curr = max(prev1, prev2 + nums[i]); shift the window.

Complexity
----------
- Time:  O(n)
- Space: O(1)   (with the two-variable rolling form)

Python solution
---------------
class Solution:
    def rob(self, nums):
        prev2 = 0   # best up to house i-2 (nothing yet)
        prev1 = 0   # best up to house i-1
        for x in nums:
            curr = max(prev1, prev2 + x)
            prev2 = prev1
            prev1 = curr
        return prev1

Interview tips
--------------
- Frame the decision FIRST: "At each house I choose rob-or-skip." That single
  sentence motivates the recurrence and the interviewer instantly knows you
  see it as DP, not greedy.
- Watch the GREEDY TRAP: always picking the biggest house, or always picking
  alternating houses, both fail. Test [2,1,1,2] -> answer 4 (pick ends), or
  [2,7,9,3,1] -> answer 12 (skip 7).
- Lead with O(n) space (the dp array) for clarity, then volunteer the O(1)
  rolling-variable refinement. Showing both signals you understand the
  "only-look-back-k" pattern.
- Initialise both rolling vars to 0 — works cleanly even for the n=1 case
  (loop runs once, returns max(0, 0 + nums[0]) = nums[0]).
- Follow-ups Microsoft often asks:
    LC 213 House Robber II  — houses arranged in a CIRCLE. Solve twice:
                              once excluding the first, once excluding the
                              last; take the max.
    LC 337 House Robber III — houses arranged as a BINARY TREE. Same
                              rob-or-skip choice, returned as a (rob, skip)
                              tuple bubbled up from each subtree.
"""
