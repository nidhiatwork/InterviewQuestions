# LeetCode #973 - K Closest Points to Origin

**Data structure:** Heap (Priority Queue)  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/k-closest-points-to-origin/

## Problem

Given `points[i] = [xi, yi]` on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)` by Euclidean distance. The answer may be returned in any order and is unique up to ordering.

## Examples

```text
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
```

```text
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]   (any order)
```

## Constraints

- `1 <= k <= points.length <= 10^4`
- `-10^4 <= xi, yi <= 10^4`

## Approach

Keep a **max-heap of size k** keyed by (negative) squared distance, so the farthest of the current `k` sits on top and is evicted when a closer point arrives.

Distance comparisons never need `sqrt` — `x^2 + y^2` preserves ordering, so compare squared distances and avoid floating point.

- For each point, push `(-(x^2 + y^2), x, y)` onto the heap.
- If the heap exceeds `k`, pop — since it's a min-heap on the **negative** distance, the popped element is the farthest, which we discard.
- After all points, the heap holds the `k` closest.

A size-`k` heap gives `O(n log k)`, better than sorting all `n` when `k << n`.

**Complexity**

- Time: `O(n log k)`
- Space: `O(k)`

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


def as_sorted_set(points):
    return sorted([list(p) for p in points])


def closest_by_distance(points, k):
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
        self.assertEqual(as_sorted_set(self.sol.kClosest(points, 3)), as_sorted_set(points))

    def test_matches_oracle(self):
        points = [[1, 3], [-2, 2], [5, 8], [0, 1], [-1, -1]]
        result = self.sol.kClosest(points, 3)
        self.assertEqual(as_sorted_set(result), as_sorted_set(closest_by_distance(points, 3)))
```

## Interview tips

- Use squared distance (`x^2 + y^2`); `sqrt` is monotonic so it never changes order, and skipping it avoids float error.
- A max-heap of size `k` keeps memory at `O(k)`; negate the distance because Python's `heapq` is a min-heap.
- `heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)` is the clean alternative, also `O(n log k)`.
- For the fastest average case, **quickselect** partitions to the `k` closest in `O(n)` — worth mentioning as the optimal follow-up.
- Sorting everything is `O(n log n)`, fine for small inputs but wasteful when `k << n`.
