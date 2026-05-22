"""LeetCode #198 — House Robber  (Array · Medium)

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
Two-state streaming. Walk the array once. At every house you carry exactly
two pieces of state from the previous step:

  take = the best total if the PREVIOUS house was robbed
  skip = the best total if the PREVIOUS house was NOT robbed

Now read the current value `x` and update:

  new_take = skip + x            # to rob now, the previous one had to be skipped
  new_skip = max(take, skip)     # to skip now, the previous one could be anything

Replace (take, skip) with (new_take, new_skip) and advance. After the last
house the answer is max(take, skip).

That's it — no table, no recurrence, no memoization. Just two numbers being
updated in lock-step with the input. It reads like a simple finite-state
machine over a stream of values.

Why this isn't greedy
---------------------
A greedy "always pick the biggest" or "always pick alternating houses" both
fail (see the GREEDY TRAP tests). The reason we get away with only two state
variables is that the choice at house i depends ONLY on whether i-1 was
taken or skipped — nothing earlier matters once those two totals are known.

Complexity
----------
- Time:  O(n)   — one pass.
- Space: O(1)   — exactly two ints.

Python solution
---------------
class Solution:
    def rob(self, nums):
        take, skip = 0, 0
        for x in nums:
            take, skip = skip + x, max(take, skip)
        return max(take, skip)

Notes on the one-liner update
-----------------------------
- The tuple-swap `take, skip = skip + x, max(take, skip)` evaluates the
  RHS before assigning, so both new values are computed from the OLD ones.
  Don't split it into two sequential statements — that overwrites `skip`
  before `new_take` is computed and corrupts the answer.
- Initialising both to 0 handles the n == 1 case automatically: after one
  iteration take = nums[0], skip = 0, max = nums[0].

Interview tips
--------------
- Frame it AS A STATE MACHINE, not as DP:
    "I'll track two totals as I walk the houses: the best total assuming I
     just robbed, and the best total assuming I just skipped. Each new house
     updates both in constant time."
  This avoids inviting follow-ups about memoization or table sizes.
- Watch the GREEDY TRAP: [2,1,1,2] -> 4 (pick ends), [2,7,9,3,1] -> 12
  (skip 7). State these out loud — it shows you tested non-trivial cases.
- Microsoft loves the follow-ups:
    LC 213 House Robber II  — houses arranged in a CIRCLE. Run the same
                              two-state pass twice: once excluding the
                              first house, once excluding the last; take
                              the max.
    LC 337 House Robber III — houses arranged as a BINARY TREE. Same
                              two-state idea: each subtree returns a
                              (take, skip) pair bubbled up post-order.
"""
