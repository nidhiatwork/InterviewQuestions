"""LeetCode #200 — Number of Islands  (Graph · Medium)

URL: https://leetcode.com/problems/number-of-islands/

Problem
-------
Given an m x n 2D binary grid of '1's (land) and '0's (water), return the
number of islands. An island is formed by connecting adjacent lands
horizontally OR vertically (NOT diagonally). All four edges of the grid are
assumed to be surrounded by water.

Examples
--------
  grid = [
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
  ]  ->  1

  grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
  ]  ->  3

Constraints
-----------
  1 <= m, n <= 300
  grid[i][j] is '0' or '1'.

Note: Each test deep-copies the input, so you may mutate `grid` in place.

Run
---
  python 2026-05-14-number-of-islands.py -v
"""

import copy
import unittest


class Solution:
    def numIslands(self, grid):
        raise NotImplementedError("Implement numIslands")


# ----------------------------- tests -----------------------------

class TestNumberOfIslands(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def _run(self, grid, expected):
        self.assertEqual(self.sol.numIslands(copy.deepcopy(grid)), expected)

    def test_example1_single_island(self):
        grid = [
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
        ]
        self._run(grid, 1)

    def test_example2_three_islands(self):
        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"],
        ]
        self._run(grid, 3)

    def test_all_water(self):
        self._run([["0", "0"], ["0", "0"]], 0)

    def test_all_land_single_island(self):
        grid = [["1"] * 4 for _ in range(4)]
        self._run(grid, 1)

    def test_diagonal_neighbors_do_not_connect(self):
        grid = [
            ["1", "0", "1", "0"],
            ["0", "1", "0", "1"],
            ["1", "0", "1", "0"],
            ["0", "1", "0", "1"],
        ]
        self._run(grid, 8)

    def test_single_cell_land(self):
        self._run([["1"]], 1)

    def test_single_cell_water(self):
        self._run([["0"]], 0)

    def test_long_strip(self):
        grid = [["1" if c % 2 == 0 else "0" for c in range(300)]]
        self._run(grid, 150)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Each '1' is a node. Two '1's are connected if they're 4-directionally
adjacent. The answer = number of connected components.

DFS flood-fill:
  1. Walk every cell.
  2. When you hit '1', increment counter and DFS from that cell, marking every
     connected '1' as visited by overwriting it to '0'.
  3. DFS explores the 4 neighbors (up/down/left/right), bounded by borders.

BFS (queue) and Union-Find also work. DFS is shortest to write; BFS is safer
on a 300x300 all-land grid (avoids deep recursion).

Complexity
----------
- Time:  O(m * n)
- Space: O(m * n) worst case (recursion stack / BFS queue when grid is one island)

Python solution (DFS, in-place marking)
---------------------------------------
class Solution:
    def numIslands(self, grid):
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0

        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
                return
            grid[r][c] = '0'
            dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count

BFS variant
-----------
from collections import deque

class Solution:
    def numIslands(self, grid):
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != '1':
                    continue
                count += 1
                queue = deque([(r, c)])
                grid[r][c] = '0'
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))
        return count

Interview tips
--------------
- State the graph framing: each cell = node, 4-connectivity = edges, answer =
  connected components.
- Mention all three approaches (DFS, BFS, Union-Find), pick one, justify.
  Bonus: note DFS recursion-depth risk on max grids; offer BFS as safer.
- In-place marking vs. visited set: trade input mutation for O(1) extra space.
  If the interviewer says "don't mutate input", switch to a visited set.
- Edge cases to call out before coding: empty, single cell, all-water,
  all-land, diagonals don't connect.
"""
