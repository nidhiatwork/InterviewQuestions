"""
LeetCode #162 - Find Peak Element  (Binary Search - Medium)
URL: https://leetcode.com/problems/find-peak-element/

Problem
-------
A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array nums, find a peak element, and return its index.
If the array contains multiple peaks, return the index to any of the peaks.

You may imagine that nums[-1] = nums[n] = -infinity. In other words, an element
is always considered to be strictly greater than a neighbor that is outside the
array.

You must write an algorithm that runs in O(log n) time.

Examples
--------
1) Input:  nums = [1,2,3,1]
   Output: 2
   Explanation: 3 is a peak element and your function should return the index
   number 2.

2) Input:  nums = [1,2,1,3,5,6,4]
   Output: 5 (or 1)
   Explanation: Your function can return either index 1 where the peak element
   is 2, or index 5 where the peak element is 6.

Constraints
-----------
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- nums[i] != nums[i + 1] for all valid i.

Run
---
    python 2026-06-16-find-peak-element.py -v
"""

import unittest


class Solution:
    def findPeakElement(self, nums):
        raise NotImplementedError("Implement findPeakElement")


def is_peak(nums, i):
    """True if nums[i] is strictly greater than its in-bounds neighbors."""
    n = len(nums)
    left_ok = i == 0 or nums[i] > nums[i - 1]
    right_ok = i == n - 1 or nums[i] > nums[i + 1]
    return left_ok and right_ok


class TestFindPeakElement(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertReturnsAPeak(self, nums):
        idx = self.sol.findPeakElement(nums)
        self.assertTrue(0 <= idx < len(nums))
        self.assertTrue(is_peak(nums, idx), f"index {idx} is not a peak in {nums}")

    def test_example_1(self):
        self.assertEqual(self.sol.findPeakElement([1, 2, 3, 1]), 2)

    def test_example_2_any_peak(self):
        self.assertReturnsAPeak([1, 2, 1, 3, 5, 6, 4])

    def test_single_element(self):
        self.assertEqual(self.sol.findPeakElement([42]), 0)

    def test_two_elements_increasing(self):
        self.assertEqual(self.sol.findPeakElement([1, 2]), 1)

    def test_two_elements_decreasing(self):
        self.assertEqual(self.sol.findPeakElement([2, 1]), 0)

    def test_strictly_increasing(self):
        self.assertEqual(self.sol.findPeakElement([1, 2, 3, 4, 5]), 4)

    def test_strictly_decreasing(self):
        self.assertEqual(self.sol.findPeakElement([5, 4, 3, 2, 1]), 0)

    def test_peak_in_middle_any(self):
        self.assertReturnsAPeak([1, 3, 2, 4, 1])

    def test_negative_values(self):
        self.assertReturnsAPeak([-5, -3, -8, -1, -10])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Binary search on the slope, not on a sorted order.

Even though the array is not sorted, we can still binary search because the
boundary conditions (nums[-1] = nums[n] = -infinity) guarantee a peak always
exists, and we can always walk "uphill" toward one.

At index mid, compare nums[mid] with nums[mid + 1]:
  - If nums[mid] < nums[mid + 1], the slope is ascending to the right, so a peak
    must exist somewhere to the right (the values keep rising and must eventually
    fall, because the right boundary is -infinity). Move lo = mid + 1.
  - Otherwise nums[mid] > nums[mid + 1], the slope descends to the right, so a
    peak exists at mid or to its left. Move hi = mid.

When lo == hi, that index is a peak. The "uphill" direction always contains a
peak, so we never miss one.

Complexity
----------
- Time:  O(log n), halving the search range each step.
- Space: O(1).

Python solution
---------------
class Solution:
    def findPeakElement(self, nums):
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1     # peak is to the right
            else:
                hi = mid         # peak is at mid or to the left
        return lo

Interview tips
--------------
- The trick is realizing binary search works without a sorted array: you binary
  search on the direction of the slope toward higher ground.
- Compare mid with mid+1 (not mid-1) to keep the index math simple and avoid
  out-of-bounds; mid+1 is always valid while lo < hi.
- Because adjacent elements are never equal and the virtual boundaries are
  -infinity, a peak is guaranteed, so no "not found" case exists.
- Always converging the range to a single index (lo == hi) avoids an explicit
  peak check inside the loop.
- A linear scan also works (return the first i where nums[i] > nums[i+1]) but
  fails the O(log n) requirement.
"""
