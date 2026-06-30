"""
LeetCode #994 - Rotting Oranges  (Graph - Medium)
URL: https://leetcode.com/problems/rotting-oranges/

Problem
-------
You are given an m x n grid where each cell can have one of three values:
  - 0 representing an empty cell,
  - 1 representing a fresh orange, or
  - 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten
orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh
orange. If this is impossible, return -1.

Examples
--------
1) Input:  grid = [[2,1,1],[1,1,0],[0,1,1]]
   Output: 4

2) Input:  grid = [[2,1,1],[0,1,1],[1,0,1]]
   Output: -1
   Explanation: The orange in the bottom left corner (row 2, column 0) is never
   rotten, because rotting only happens 4-directionally.

3) Input:  grid = [[0,2]]
   Output: 0
   Explanation: Since there are already no fresh oranges at minute 0, the answer
   is just 0.

Constraints
-----------
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2.

Run
---
    python 2026-06-30-rotting-oranges.py -v
"""

from collections import deque
import unittest


class Solution:
    def orangesRotting(self, grid):
        raise NotImplementedError("Implement orangesRotting")


class TestOrangesRotting(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(
            self.sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]), 4
        )

    def test_example_2_impossible(self):
        self.assertEqual(
            self.sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]), -1
        )

    def test_example_3_no_fresh(self):
        self.assertEqual(self.sol.orangesRotting([[0, 2]]), 0)

    def test_all_empty(self):
        self.assertEqual(self.sol.orangesRotting([[0, 0], [0, 0]]), 0)

    def test_single_fresh_no_rotten(self):
        self.assertEqual(self.sol.orangesRotting([[1]]), -1)

    def test_single_rotten(self):
        self.assertEqual(self.sol.orangesRotting([[2]]), 0)

    def test_all_rotten_already(self):
        self.assertEqual(self.sol.orangesRotting([[2, 2], [2, 2]]), 0)

    def test_one_step(self):
        self.assertEqual(self.sol.orangesRotting([[2, 1]]), 1)

    def test_isolated_fresh_by_empty(self):
        # fresh orange separated by empty cell from rotten -> impossible
        self.assertEqual(self.sol.orangesRotting([[2, 0, 1]]), -1)

    def test_column_spread(self):
        self.assertEqual(
            self.sol.orangesRotting([[2], [1], [1], [1]]), 3
        )


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Multi-source BFS. All initially rotten oranges spread simultaneously, so seed the
queue with EVERY rotten orange at minute 0 and expand level by level; the number
of BFS levels is the elapsed minutes.

Setup:
  - Scan the grid once. Push every rotten orange (r, c) into the queue. Count the
    number of FRESH oranges.
  - If there are no fresh oranges at the start, return 0 immediately.

BFS by minute:
  - Process the queue in level order. Each level represents one minute. For every
    rotten orange at the current level, look at its 4 neighbors; any fresh
    neighbor becomes rotten, is decremented from the fresh count, and is enqueued
    for the next level.
  - Increment the minute counter once per level that actually rots something.

At the end, if any fresh oranges remain (fresh > 0) they were unreachable -> return
-1. Otherwise return the minute counter.

Multi-source BFS is the key: starting all rotten oranges together naturally
computes the time for the LAST orange to rot, because BFS explores in order of
distance (minutes) from the nearest source.

Complexity
----------
- Time:  O(m * n), each cell enqueued/processed at most once.
- Space: O(m * n) for the queue in the worst case.

Python solution
---------------
from collections import deque


class Solution:
    def orangesRotting(self, grid):
        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:
            return 0

        minutes = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):       # process exactly one minute's worth
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))

        return minutes if fresh == 0 else -1

Interview tips
--------------
- Multi-source BFS: enqueue ALL rotten oranges first so they spread in parallel;
  a single-source BFS per orange would be wrong and slower.
- Track the fresh count and decrement as you rot; the final fresh > 0 check is how
  you detect the impossible (-1) case.
- Process the queue one LEVEL at a time (snapshot len(queue)); each level is one
  minute.
- Handle the "no fresh at start" case up front - the answer is 0, not the number
  of BFS levels.
- Empty cells (0) act as walls; oranges separated from all rotten sources by 0s
  or grid edges can never rot.
"""
