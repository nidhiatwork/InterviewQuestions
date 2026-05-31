"""LeetCode #153 — Find Minimum in Rotated Sorted Array  (Binary Search · Medium)

URL: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Problem
-------
Suppose an array of length n sorted in ascending order is rotated between 1
and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:
  [4,5,6,7,0,1,2] if it was rotated 4 times.
  [0,1,2,4,5,6,7] if it was rotated 7 times.

Given the sorted rotated array nums of unique elements, return the minimum
element of this array.

You must write an algorithm that runs in O(log n) time.

Examples
--------
  nums = [3,4,5,1,2]            ->  1
  nums = [4,5,6,7,0,1,2]        ->  0
  nums = [11,13,15,17]          ->  11   (not rotated / rotated n times)
  nums = [2,1]                  ->  1

Constraints
-----------
  n == nums.length
  1 <= n <= 5000
  -5000 <= nums[i] <= 5000
  All the integers of nums are unique.
  nums is sorted and rotated between 1 and n times.

Run
---
  python 2026-05-31-find-minimum-in-rotated-sorted-array.py -v
"""

import unittest


class Solution:
    def findMin(self, nums):
        raise NotImplementedError("Implement findMin")


# ----------------------------- tests -----------------------------

class TestFindMin(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.findMin([3, 4, 5, 1, 2]), 1)

    def test_example_2(self):
        self.assertEqual(self.sol.findMin([4, 5, 6, 7, 0, 1, 2]), 0)

    def test_not_rotated(self):
        self.assertEqual(self.sol.findMin([11, 13, 15, 17]), 11)

    def test_two_elements_rotated(self):
        self.assertEqual(self.sol.findMin([2, 1]), 1)

    def test_two_elements_sorted(self):
        self.assertEqual(self.sol.findMin([1, 2]), 1)

    def test_single_element(self):
        self.assertEqual(self.sol.findMin([7]), 7)

    def test_rotated_by_one(self):
        self.assertEqual(self.sol.findMin([5, 1, 2, 3, 4]), 1)

    def test_rotated_by_n_minus_one(self):
        self.assertEqual(self.sol.findMin([2, 3, 4, 5, 1]), 1)

    def test_with_negative_numbers(self):
        self.assertEqual(self.sol.findMin([3, 4, 5, -3, -2, -1, 0, 1, 2]), -3)

    def test_pivot_in_middle(self):
        self.assertEqual(self.sol.findMin([6, 7, 8, 9, 10, 1, 2, 3, 4, 5]), 1)

    def test_min_is_last_after_long_left_run(self):
        # Confirms we don't accidentally return nums[0] when the "rotated by n"
        # case looks similar to a long sorted-left case.
        self.assertEqual(self.sol.findMin([4, 5, 1, 2, 3]), 1)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
A rotated sorted array of unique values is two ascending runs joined at a
"pivot." The minimum sits at the start of the second run — i.e., it's the
ONLY index i where nums[i-1] > nums[i] (or i == 0 if the array isn't really
rotated).

You don't need to find the pivot index — you only need its value. Standard
trick: at each step compare nums[mid] against nums[hi]:

  - If nums[mid] > nums[hi], the minimum lies strictly to the RIGHT of mid
    (the pivot is in (mid, hi]). Move lo = mid + 1.
  - Otherwise nums[mid] <= nums[hi], so the minimum lies AT mid or to its
    LEFT. Move hi = mid (NOT mid - 1 — mid itself might be the answer).

Loop while lo < hi. When the loop exits, lo == hi and that index holds the
minimum. Comparing against nums[hi] (not nums[lo]) is what makes the
"already sorted / not rotated" case fall out naturally — nums[mid] <=
nums[hi] keeps shrinking hi toward 0, returning nums[0].

The unique-values constraint matters: with duplicates this becomes #154
(worst case O(n)).

Complexity
----------
- Time:  O(log n)   classic binary search
- Space: O(1)

Python solution
---------------
class Solution:
    def findMin(self, nums):
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                # Pivot lies to the right of mid.
                lo = mid + 1
            else:
                # nums[mid] <= nums[hi]; minimum is at mid or to its left.
                hi = mid
        return nums[lo]

Interview tips
--------------
- The first sentence to say out loud: "The minimum is the start of the
  second sorted run; the predicate is monotone, so binary search works."
- Compare against nums[hi], not nums[lo]. Comparing against nums[lo] forces
  you to handle the "already sorted" case as a special branch up front.
  Comparing against nums[hi] folds it in for free.
- Move hi = mid, NOT hi = mid - 1. mid itself might be the minimum. This
  is the classic off-by-one to call out before you write the line.
- Loop invariant: the minimum always lies in [lo, hi]. The loop ends when
  lo == hi, so return nums[lo] (== nums[hi]). No post-loop comparison needed.
- The unique-elements constraint is load-bearing. If asked about duplicates
  (#154), the same skeleton works, but the nums[mid] == nums[hi] case
  forces hi -= 1 instead of a halving step — worst case O(n). Mention it.
- Microsoft follow-up: "now also return the rotation count." Answer: it's
  just the index of the minimum (lo at the end). Free extension.
- Don't compute mid = (lo + hi) / 2 in languages with fixed-width int —
  use lo + (hi - lo) // 2 to avoid overflow. In Python it doesn't matter,
  but it's good to mention.
"""
