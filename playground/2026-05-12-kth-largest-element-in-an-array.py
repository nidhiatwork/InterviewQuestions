"""LeetCode #215 — Kth Largest Element in an Array  (Heap · Medium)

URL: https://leetcode.com/problems/kth-largest-element-in-an-array/

Problem
-------
Given an integer array `nums` and an integer `k`, return the k-th largest
element in the array (k-th largest in sorted order, NOT k-th distinct).

The interview-expected first answer is O(n log k) using a min-heap of size k.
A Quickselect implementation gives expected O(n) as a follow-up.

Examples
--------
  nums = [3,2,1,5,6,4],         k = 2  ->  5
  nums = [3,2,3,1,2,4,5,5,6],   k = 4  ->  4

Constraints
-----------
  1 <= k <= nums.length <= 10^5
  -10^4 <= nums[i] <= 10^4

Run
---
  python 2026-05-12-kth-largest-element-in-an-array.py -v
"""

import unittest


class Solution:
    def findKthLargest(self, nums, k):
        raise NotImplementedError("Implement findKthLargest")


# ----------------------------- tests -----------------------------

class TestKthLargest(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.findKthLargest([3, 2, 1, 5, 6, 4], 2), 5)

    def test_example_2(self):
        self.assertEqual(self.sol.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)

    def test_single_element_k_equals_one(self):
        self.assertEqual(self.sol.findKthLargest([1], 1), 1)

    def test_k_equals_length(self):
        # k == n  =>  the smallest element.
        self.assertEqual(self.sol.findKthLargest([7, 1, 3, 5], 4), 1)

    def test_all_duplicates(self):
        self.assertEqual(self.sol.findKthLargest([2, 2, 2, 2], 2), 2)

    def test_negative_numbers(self):
        self.assertEqual(self.sol.findKthLargest([-1, -5, -3, -2, -4], 2), -2)

    def test_large_sorted(self):
        nums = list(range(1, 101))
        self.assertEqual(self.sol.findKthLargest(nums, 1), 100)
        self.assertEqual(self.sol.findKthLargest(nums, 50), 51)
        self.assertEqual(self.sol.findKthLargest(nums, 100), 1)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Min-heap of size k.
  1. Push the first k elements onto a min-heap. The root is the smallest of
     those k.
  2. For each remaining element, if it's larger than the root, replace the
     root (heapreplace).
  3. At the end, the root is the k-th largest.

Why a min-heap of size k (not max-heap of size n)? You only need to track the
top-k candidates seen so far. The smallest of those candidates lives at the
root and is the threshold for whether a new element qualifies. Space stays at
O(k) instead of O(n).

Complexity
----------
- Time:  O(n log k)
- Space: O(k)

Python solution
---------------
import heapq

class Solution:
    def findKthLargest(self, nums, k):
        heap = []
        for n in nums:
            if len(heap) < k:
                heapq.heappush(heap, n)
            elif n > heap[0]:
                heapq.heapreplace(heap, n)
        return heap[0]

Quickselect (O(n) expected) — bonus
-----------------------------------
import random

class Solution:
    def findKthLargest(self, nums, k):
        target = len(nums) - k  # (n - k)-th smallest, 0-indexed

        def quickselect(lo, hi):
            pivot = nums[random.randint(lo, hi)]
            lt, eq, gt = lo, lo, hi
            i = lo
            while i <= gt:
                if nums[i] < pivot:
                    nums[lt], nums[i] = nums[i], nums[lt]
                    lt += 1; eq += 1; i += 1
                elif nums[i] > pivot:
                    nums[gt], nums[i] = nums[i], nums[gt]
                    gt -= 1
                else:
                    eq += 1; i += 1
            if target < lt:  return quickselect(lo, lt - 1)
            if target >= eq: return quickselect(eq, hi)
            return pivot

        return quickselect(0, len(nums) - 1)

Interview tips
--------------
- Lead with the min-heap-of-size-k approach. Articulate the invariant
  ("root is the smallest of top-k seen so far"). O(k) space is the win.
- Use heapreplace, not heappush + heappop — one sift instead of two.
- Mention Quickselect for the O(n) follow-up. Worst-case O(n^2) without a
  randomized pivot; median-of-medians for guaranteed O(n).
- Edge cases: k == n (returns min), duplicates, negatives.
"""
