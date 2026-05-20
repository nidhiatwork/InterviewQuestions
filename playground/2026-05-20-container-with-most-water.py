"""LeetCode #11 — Container With Most Water  (Array · Medium)

URL: https://leetcode.com/problems/container-with-most-water/

Problem
-------
You are given an integer array `height` of length n. There are n vertical lines
drawn such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Examples
--------
  height = [1,8,6,2,5,4,8,3,7]  -> 49
      (lines at index 1 and 8: width=7, min(8,7)=7  -> 7*7 = 49)
  height = [1,1]                -> 1
      (lines at index 0 and 1: width=1, min(1,1)=1  -> 1*1 = 1)

Constraints
-----------
  n == height.length
  2 <= n <= 10^5
  0 <= height[i] <= 10^4

Run
---
  python 2026-05-20-container-with-most-water.py -v
"""

import unittest


class Solution:
    def maxArea(self, height):
        raise NotImplementedError("Implement maxArea")


# ----------------------------- tests -----------------------------

class TestMaxArea(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_example_2_minimum_length(self):
        self.assertEqual(self.sol.maxArea([1, 1]), 1)

    def test_two_equal_tall(self):
        # width=1, height=min(7,7)=7 -> 7
        self.assertEqual(self.sol.maxArea([7, 7]), 7)

    def test_increasing(self):
        # Best is (0, n-1): width=4, height=min(1,5)=1 -> 4.
        # Or (3,4): width=1, height=4 -> 4. Both give 4.
        self.assertEqual(self.sol.maxArea([1, 2, 3, 4, 5]), 6)
        # Recheck: heights[1..4]: (1,4): w=3 h=min(2,5)=2 -> 6. Yes 6.

    def test_decreasing(self):
        # Mirror of increasing: (0,3) w=3 h=min(5,2)=2 -> 6.
        self.assertEqual(self.sol.maxArea([5, 4, 3, 2, 1]), 6)

    def test_all_same(self):
        # Best width wins when heights are equal: w=4 * h=3 = 12.
        self.assertEqual(self.sol.maxArea([3, 3, 3, 3, 3]), 12)

    def test_zero_heights_at_ends(self):
        # (0,5): h=0 -> 0. Best is (1,4): w=3, h=min(5,5)=5 -> 15.
        self.assertEqual(self.sol.maxArea([0, 5, 4, 3, 5, 0]), 15)

    def test_single_tall_in_middle(self):
        # (0,4): w=4, h=min(1,1)=1 -> 4. (1,4): 3*1=3. The tall middle helps
        # only via width with the ends. Best = (0,4) = 4.
        self.assertEqual(self.sol.maxArea([1, 1, 10, 1, 1]), 4)

    def test_large_uniform(self):
        # 10^4 lines of height 10^4: w=9999, h=10000 -> 99,990,000.
        self.assertEqual(self.sol.maxArea([10000] * 10000), 99990000)

    def test_left_taller_than_right(self):
        # (0,4): w=4, h=min(8,2)=2 -> 8. (0,3): w=3, h=min(8,3)=3 -> 9.
        # (0,2): w=2, h=min(8,4)=4 -> 8. (0,1): w=1, h=min(8,5)=5 -> 5.
        # Best = 9.
        self.assertEqual(self.sol.maxArea([8, 5, 4, 3, 2]), 9)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Two pointers, one at each end. The area between them is:

    area = (right - left) * min(height[left], height[right])

At every step, move the pointer at the SHORTER line inward by one. Why?
Because the area is limited by the shorter line. Keeping the shorter line and
moving the taller one inward shrinks the width AND can never give a larger
height (min still capped by the same short line) — so that move can never
improve things. Moving the shorter line is the only way to possibly find a
taller minimum.

Algorithm
---------
left, right = 0, n - 1
best = 0
while left < right:
    h = min(height[left], height[right])
    best = max(best, (right - left) * h)
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
return best

Why O(n) works
--------------
Brute force is O(n^2): try every pair. Two-pointer is O(n) because each
iteration advances exactly one pointer, so total iterations <= n - 1.

The correctness argument is the key insight: when we discard the shorter side,
we don't miss anything. Every pair we skip would have used that short line as
the bottleneck, so its area can't exceed what we already computed for the
widest pair involving that short line.

Complexity
----------
- Time:  O(n)
- Space: O(1)

Python solution
---------------
class Solution:
    def maxArea(self, height):
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            h = min(height[left], height[right])
            best = max(best, (right - left) * h)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best

Interview tips
--------------
- Lead with the CORRECTNESS argument, not the code. "Area is bounded by the
  shorter line. Moving the taller line inward can't help — so we always move
  the shorter one." Stating this up front earns the problem.
- Don't confuse this with TRAPPING RAIN WATER (LC 42). That problem also uses
  two pointers but asks for the total trapped volume across ALL valleys; this
  one asks for the SINGLE pair of lines that maximises width * min-height.
- Tie-breaker when height[left] == height[right]: either pointer can move.
  In the code above the `else` branch covers equality (moves right). It
  doesn't matter for the answer.
- Watch the formula: width is the INDEX difference (right - left), not the
  cell count. Off-by-one here is a common slip.
- Follow-up Microsoft sometimes asks: "Return the two indices, not the area."
  Same loop, just track (left, right) at every `best` update.
"""
