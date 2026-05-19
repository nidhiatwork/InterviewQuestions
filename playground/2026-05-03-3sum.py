"""LeetCode #15 — 3Sum  (Array · Medium)

URL: https://leetcode.com/problems/3sum/

Problem
-------
Given an integer array `nums`, return all the triplets [nums[i], nums[j], nums[k]] such that:
  - i != j, i != k, j != k, AND
  - nums[i] + nums[j] + nums[k] == 0.

The solution set must NOT contain duplicate triplets.

Examples
--------
  nums = [-1, 0, 1, 2, -1, -4]  ->  [[-1, -1, 2], [-1, 0, 1]]
  nums = [0, 1, 1]              ->  []
  nums = [0, 0, 0]              ->  [[0, 0, 0]]

Constraints
-----------
  3 <= nums.length <= 3000
  -10^5 <= nums[i] <= 10^5

Run
---
  python 2026-05-03-3sum.py -v
"""

import unittest


class Solution:
    def threeSum(self, nums):
        raise NotImplementedError("Implement threeSum")


# ----------------------------- tests -----------------------------

class TestThreeSum(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    @staticmethod
    def _normalize(triplets):
        return sorted(sorted(t) for t in triplets)

    def test_example_1_basic(self):
        self.assertEqual(
            self._normalize(self.sol.threeSum([-1, 0, 1, 2, -1, -4])),
            self._normalize([[-1, -1, 2], [-1, 0, 1]]),
        )

    def test_example_2_no_triplet(self):
        self.assertEqual(self.sol.threeSum([0, 1, 1]), [])

    def test_example_3_all_zeros(self):
        self.assertEqual(self.sol.threeSum([0, 0, 0]), [[0, 0, 0]])

    def test_minimum_input_size(self):
        self.assertEqual(self.sol.threeSum([1, 2, 3]), [])

    def test_minimum_input_size_with_solution(self):
        self.assertEqual(self.sol.threeSum([-1, 0, 1]), [[-1, 0, 1]])

    def test_all_negatives(self):
        self.assertEqual(self.sol.threeSum([-5, -4, -3, -2, -1]), [])

    def test_many_duplicates(self):
        self.assertEqual(
            self._normalize(self.sol.threeSum([0, 0, 0, 0, -1, 1])),
            self._normalize([[-1, 0, 1], [0, 0, 0]]),
        )

    def test_duplicate_triplets_are_deduped(self):
        self.assertEqual(
            self._normalize(self.sol.threeSum([-2, 0, 0, 2, 2])),
            self._normalize([[-2, 0, 2]]),
        )

    def test_large_input_performance(self):
        import random
        random.seed(42)
        nums = [random.randint(-50, 50) for _ in range(297)]
        nums += [-1, -2, 3]
        result = self.sol.threeSum(nums)
        for t in result:
            self.assertEqual(len(t), 3)
            self.assertEqual(sum(t), 0)
        self.assertEqual(len(result), len({tuple(sorted(t)) for t in result}))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Sort + outer loop + two-pointer scan. The naive triple loop is O(n^3); sorting
lets us (a) skip duplicates trivially and (b) use two pointers to find pairs
that sum to a target in linear time.

1. Sort nums ascending.
2. For each i in [0, n-3]:
     - If nums[i] > 0, break  (smallest already positive => no zero-sum).
     - If i > 0 and nums[i] == nums[i-1], skip (dedupe first element).
     - target = -nums[i]; lo, hi = i+1, n-1.
       - if nums[lo] + nums[hi] == target: record, then advance past dupes.
       - if sum < target: lo += 1
       - if sum > target: hi -= 1

Complexity
----------
- Time:  O(n^2)
- Space: O(1) extra (excluding the output and sort's recursion stack).

Python solution
---------------
class Solution:
    def threeSum(self, nums):
        nums.sort()
        n = len(nums)
        result = []
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            target = -nums[i]
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[lo] + nums[hi]
                if s == target:
                    result.append([nums[i], nums[lo], nums[hi]])
                    while lo < hi and nums[lo] == nums[lo + 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi - 1]:
                        hi -= 1
                    lo += 1
                    hi -= 1
                elif s < target:
                    lo += 1
                else:
                    hi -= 1
        return result

Interview tips (what Microsoft is watching for)
-----------------------------------------------
- Sort first. Most candidates jump to a hash-set; the two-pointer-after-sort
  is more space-efficient and generalises cleanly to kSum.
- Duplicate handling is the hard part. The two inner `while ... nums[lo] ==
  nums[lo+1]` loops trip people up — walk through them with a duplicate-heavy
  input on the whiteboard.
- State complexity: O(n^2) time, O(1) extra space (excluding output).
- Edge cases without prompting: n < 3, all zeros, all positives, all
  negatives, very large inputs.
- Follow-up: "kSum?" recursion + base case at twoSum. "Without sorting?"
  hash-set with O(n^2) time + O(n) space (harder to dedupe).
"""
