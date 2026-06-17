"""
LeetCode #300 - Longest Increasing Subsequence  (Binary Search - Medium)
URL: https://leetcode.com/problems/longest-increasing-subsequence/

Problem
-------
Given an integer array nums, return the length of the longest strictly
increasing subsequence.

A subsequence is a sequence that can be derived from the array by deleting some
or no elements without changing the order of the remaining elements.

Examples
--------
1) Input:  nums = [10,9,2,5,3,7,101,18]
   Output: 4
   Explanation: The longest increasing subsequence is [2,3,7,101], so the length
   is 4.

2) Input:  nums = [0,1,0,3,2,3]
   Output: 4
   Explanation: One LIS is [0,1,2,3].

3) Input:  nums = [7,7,7,7,7,7,7]
   Output: 1
   Explanation: The longest strictly increasing subsequence is any single 7.

Constraints
-----------
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

Follow-up
---------
Can you come up with an algorithm that runs in O(n log n) time?

Run
---
    python 2026-06-17-longest-increasing-subsequence.py -v
"""

import unittest


class Solution:
    def lengthOfLIS(self, nums):
        raise NotImplementedError("Implement lengthOfLIS")


class TestLengthOfLIS(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]), 4)

    def test_example_2(self):
        self.assertEqual(self.sol.lengthOfLIS([0, 1, 0, 3, 2, 3]), 4)

    def test_all_equal(self):
        self.assertEqual(self.sol.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]), 1)

    def test_single_element(self):
        self.assertEqual(self.sol.lengthOfLIS([5]), 1)

    def test_strictly_increasing(self):
        self.assertEqual(self.sol.lengthOfLIS([1, 2, 3, 4, 5]), 5)

    def test_strictly_decreasing(self):
        self.assertEqual(self.sol.lengthOfLIS([5, 4, 3, 2, 1]), 1)

    def test_with_negatives(self):
        self.assertEqual(self.sol.lengthOfLIS([-2, -1, 0, -3, 5, 4]), 4)

    def test_two_increasing(self):
        self.assertEqual(self.sol.lengthOfLIS([1, 3]), 2)

    def test_duplicates_break_run(self):
        # strictly increasing, so equal neighbors do not extend
        self.assertEqual(self.sol.lengthOfLIS([1, 3, 3, 3, 4]), 3)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Maintain a running "tails" array using a greedy rule plus binary search
(the patience-sorting idea).

Walk through nums once. Keep a list `tails`, where tails[i] is the SMALLEST
possible tail value of any increasing subsequence of length i + 1 seen so far.
This list is always sorted, which is what lets us binary search it.

For each number x:
  - Binary search tails for the leftmost position whose value is >= x.
  - If we find such a position, overwrite it with x. This keeps that
    subsequence-length's tail as small as possible, leaving more room to extend
    later.
  - If x is larger than every tail, append it - we have extended the best run by
    one, so the answer grows.

The length of `tails` at the end is the LIS length. Note tails is NOT an actual
subsequence, just a compact summary of the best achievable tails; its LENGTH is
what matters.

Why it works: keeping each length's tail as small as possible is always at least
as good as keeping a larger tail, because a smaller tail can be extended by more
future values. The sorted invariant makes each insertion an O(log n) binary
search.

Complexity
----------
- Time:  O(n log n), one binary search per element.
- Space: O(n) for the tails list.

Python solution
---------------
import bisect


class Solution:
    def lengthOfLIS(self, nums):
        tails = []
        for x in nums:
            pos = bisect.bisect_left(tails, x)   # leftmost tail >= x
            if pos == len(tails):
                tails.append(x)                  # x extends the longest run
            else:
                tails[pos] = x                   # keep this length's tail minimal
        return len(tails)

Interview tips
--------------
- Frame it as a streaming/greedy method: scan once, keep the smallest tail for
  each achievable length, and binary search to place each value.
- bisect_left gives STRICTLY increasing (it replaces an equal value, so
  duplicates do not extend the run). For non-strict (allow equal), use
  bisect_right.
- Emphasize that `tails` is not the subsequence itself - only its length is the
  answer. Reconstructing the actual subsequence needs extra index bookkeeping.
- The simpler O(n^2) approach (for each i, scan all j < i) is fine to mention as
  a baseline, but the tails + binary search method hits the O(n log n) follow-up.
- Watch the strict-vs-non-strict distinction; it is the most common bug here.
"""
