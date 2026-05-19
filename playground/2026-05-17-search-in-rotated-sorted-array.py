"""LeetCode #33 — Search in Rotated Sorted Array  (Binary Search · Medium)

URL: https://leetcode.com/problems/search-in-rotated-sorted-array/

Problem
-------
There is an integer array `nums` sorted in ascending order (with distinct values).
Prior to being passed to your function, `nums` is possibly rotated at an unknown
pivot index k (0 <= k < len(nums)) so that the resulting array is:
    [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]
(0-indexed). For example, [0,1,2,4,5,6,7] rotated at pivot index 3 becomes
[4,5,6,7,0,1,2].

Given the array `nums` after the possible rotation and an integer `target`,
return the index of `target` if it is in `nums`, or -1 if it is not.

You must write an algorithm with O(log n) runtime complexity.

Examples
--------
  nums = [4,5,6,7,0,1,2], target = 0   ->  4
  nums = [4,5,6,7,0,1,2], target = 3   ->  -1
  nums = [1],             target = 0   ->  -1

Constraints
-----------
  1 <= nums.length <= 5000
  -10^4 <= nums[i] <= 10^4
  All values of nums are unique.
  nums is guaranteed to be rotated at some pivot (possibly k = 0).
  -10^4 <= target <= 10^4

Run
---
  python 2026-05-17-search-in-rotated-sorted-array.py -v
"""

import unittest


class Solution:
    def search(self, nums, target):
        raise NotImplementedError("Implement search")


# ----------------------------- tests -----------------------------

class TestSearchRotated(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1_target_in_right_half(self):
        self.assertEqual(self.sol.search([4, 5, 6, 7, 0, 1, 2], 0), 4)

    def test_example_2_target_missing(self):
        self.assertEqual(self.sol.search([4, 5, 6, 7, 0, 1, 2], 3), -1)

    def test_example_3_single_element_missing(self):
        self.assertEqual(self.sol.search([1], 0), -1)

    def test_single_element_present(self):
        self.assertEqual(self.sol.search([1], 1), 0)

    def test_no_rotation(self):
        # k == 0: array is just sorted ascending.
        self.assertEqual(self.sol.search([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(self.sol.search([1, 2, 3, 4, 5], 1), 0)
        self.assertEqual(self.sol.search([1, 2, 3, 4, 5], 5), 4)
        self.assertEqual(self.sol.search([1, 2, 3, 4, 5], 6), -1)

    def test_target_at_pivot_boundaries(self):
        nums = [4, 5, 6, 7, 0, 1, 2]
        self.assertEqual(self.sol.search(nums, 7), 3)   # last of left half
        self.assertEqual(self.sol.search(nums, 4), 0)   # first of left half
        self.assertEqual(self.sol.search(nums, 2), 6)   # last of right half

    def test_target_in_left_half(self):
        self.assertEqual(self.sol.search([4, 5, 6, 7, 0, 1, 2], 5), 1)

    def test_two_elements_rotated(self):
        self.assertEqual(self.sol.search([3, 1], 1), 1)
        self.assertEqual(self.sol.search([3, 1], 3), 0)
        self.assertEqual(self.sol.search([3, 1], 2), -1)

    def test_negative_numbers(self):
        # [-5,-3,-1,1,3] rotated -> [1,3,-5,-3,-1]
        self.assertEqual(self.sol.search([1, 3, -5, -3, -1], -5), 2)
        self.assertEqual(self.sol.search([1, 3, -5, -3, -1], 3), 1)
        self.assertEqual(self.sol.search([1, 3, -5, -3, -1], 0), -1)

    def test_large_rotation_near_end(self):
        # [1,2,3,4,5,6,7,8] rotated at k=7 -> [8,1,2,3,4,5,6,7]
        nums = [8, 1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(self.sol.search(nums, 8), 0)
        self.assertEqual(self.sol.search(nums, 7), 7)
        self.assertEqual(self.sol.search(nums, 4), 3)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Modified binary search. Even though the whole array isn't sorted, at every
midpoint EXACTLY ONE of the two halves [lo..mid] and [mid..hi] is sorted.
That half is sorted iff its first element <= its last element.

Algorithm
---------
lo, hi = 0, n - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid

    # Decide which side is sorted.
    if nums[lo] <= nums[mid]:        # LEFT half [lo..mid] is sorted
        if nums[lo] <= target < nums[mid]:   # target lies inside it
            hi = mid - 1
        else:
            lo = mid + 1
    else:                            # RIGHT half [mid..hi] is sorted
        if nums[mid] < target <= nums[hi]:
            lo = mid + 1
        else:
            hi = mid - 1
return -1

Why this works
--------------
A rotated sorted array always has the shape of two ascending runs glued
together. Split at any mid: the pivot is in only one of the two halves, so
the OTHER half is fully sorted. Once you know which half is sorted, you can
test in O(1) whether the target is inside its [low, high] range — if yes,
binary-search there; otherwise, binary-search the other half.

The `nums[lo] <= nums[mid]` check (with <=) handles the case mid == lo
(2-element windows) correctly.

Complexity
----------
- Time:  O(log n)   each iteration halves the search window
- Space: O(1)

Python solution
---------------
class Solution:
    def search(self, nums, target):
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid

            if nums[lo] <= nums[mid]:        # left half is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                            # right half is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1

Interview tips
--------------
- Lead with the KEY invariant: "At every step, one of the two halves is
  fully sorted." That single observation collapses the whole problem.
- The `<=` (not `<`) in `nums[lo] <= nums[mid]` matters — when the window
  shrinks to 2 elements and lo == mid, the left half is trivially sorted.
- Inclusive bounds inside the if-checks: `nums[lo] <= target < nums[mid]`
  and `nums[mid] < target <= nums[hi]`. Off-by-ones here are the most
  common bug. Trace [4,5,6,7,0,1,2] looking for 0 by hand once.
- Follow-up Microsoft sometimes asks: "What if duplicates are allowed?"
  That's LC 81 — the `nums[lo] == nums[mid]` ambiguity forces a worst-case
  O(n) fallback (advance lo by 1).
- Alternative approach: first binary-search to find the pivot index, then
  binary-search the correct half. Two passes but conceptually simpler.
  Mention it as a backup if you blank on the one-pass version.
"""
