"""
LeetCode #973 - K Closest Points to Origin  (Heap (Priority Queue) - Medium)
URL: https://leetcode.com/problems/k-closest-points-to-origin/

Problem
-------
Given an array of points where points[i] = [xi, yi] represents a point on the
X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance
(i.e., sqrt((x1 - x2)^2 + (y1 - y2)^2)).

You may return the answer in any order. The answer is guaranteed to be unique
(except for the order that it is in).

Examples
--------
1) Input:  points = [[1,3],[-2,2]], k = 1
   Output: [[-2,2]]
   Explanation: distance of (1,3) is sqrt(10), of (-2,2) is sqrt(8). k=1 -> the
   closest is [-2,2].

2) Input:  points = [[3,3],[5,-1],[-2,4]], k = 2
   Output: [[3,3],[-2,4]] (any order)

Constraints
-----------
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4

Run
---
    python 2026-06-29-k-closest-points-to-origin.py -v
"""

import unittest


class Solution:
    def kClosest(self, points, k):
        raise NotImplementedError("Implement kClosest")


def as_sorted_set(points):
    """Order-independent comparison of a list of points."""
    return sorted([list(p) for p in points])


def closest_by_distance(points, k):
    """Reference oracle: sort by squared distance, take first k."""
    return sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]


class TestKClosest(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.kClosest([[1, 3], [-2, 2]], 1), [[-2, 2]])

    def test_example_2_any_order(self):
        result = self.sol.kClosest([[3, 3], [5, -1], [-2, 4]], 2)
        self.assertEqual(as_sorted_set(result), as_sorted_set([[3, 3], [-2, 4]]))

    def test_k_equals_all(self):
        points = [[1, 1], [2, 2], [3, 3]]
        result = self.sol.kClosest(points, 3)
        self.assertEqual(as_sorted_set(result), as_sorted_set(points))

    def test_single_point(self):
        self.assertEqual(self.sol.kClosest([[0, 0]], 1), [[0, 0]])

    def test_origin_included(self):
        result = self.sol.kClosest([[0, 0], [5, 5], [1, 0]], 2)
        self.assertEqual(as_sorted_set(result), as_sorted_set([[0, 0], [1, 0]]))

    def test_matches_oracle(self):
        points = [[1, 3], [-2, 2], [5, 8], [0, 1], [-1, -1]]
        result = self.sol.kClosest(points, 3)
        self.assertEqual(as_sorted_set(result), as_sorted_set(closest_by_distance(points, 3)))

    def test_negatives(self):
        points = [[-5, 4], [-6, -5], [4, 6]]
        result = self.sol.kClosest(points, 1)
        self.assertEqual(as_sorted_set(result), as_sorted_set([[-5, 4]]))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Keep a max-heap of size k keyed by (negative) squared distance, so the farthest
of the current k sits on top and is evicted when a closer point arrives.

Distance comparisons never need the actual sqrt - x^2 + y^2 preserves ordering,
so compare squared distances to avoid floating point.

  - For each point, push (-(x^2 + y^2), point) onto a heap.
  - If the heap grows beyond k, pop - because it is a min-heap on the NEGATIVE
    distance, the popped element is the one with the largest true distance, i.e.
    the farthest, which we want to discard.
  - After processing all points, the heap holds the k closest; return their
    points.

Keeping the heap at size k gives O(n log k), better than sorting all n points
when k << n. (heapq.nsmallest with key=distance is the clean one-liner with the
same complexity.)

Complexity
----------
- Time:  O(n log k), one push/pop per point on a size-k heap.
- Space: O(k) for the heap.

Python solution
---------------
import heapq


class Solution:
    def kClosest(self, points, k):
        heap = []
        for x, y in points:
            dist = x * x + y * y
            heapq.heappush(heap, (-dist, x, y))   # max-heap via negation
            if len(heap) > k:
                heapq.heappop(heap)               # drop the farthest
        return [[x, y] for _, x, y in heap]

Interview tips
--------------
- Use squared distance (x^2 + y^2); sqrt is monotonic so it never changes the
  order, and skipping it avoids float error.
- A max-heap of size k keeps memory at O(k); negate the distance because Python's
  heapq is a min-heap.
- heapq.nsmallest(k, points, key=lambda p: p[0]**2+p[1]**2) is the clean
  alternative, also O(n log k).
- For the absolute fastest average case, quickselect partitions to the k closest
  in O(n) average time - worth mentioning as the optimal follow-up.
- Sorting everything is O(n log n) and fine for small inputs but wasteful when
  k << n.
"""
