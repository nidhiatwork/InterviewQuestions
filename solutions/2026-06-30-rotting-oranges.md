# LeetCode #994 - Rotting Oranges

**Data structure:** Graph  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/rotting-oranges/

## Problem

An `m x n` grid has cells valued `0` (empty), `1` (fresh orange), or `2` (rotten orange). Every minute, any fresh orange 4-directionally adjacent to a rotten one becomes rotten.

Return the minimum minutes until no fresh orange remains, or `-1` if impossible.

## Examples

```text
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
```

```text
Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1   (bottom-left orange never rots)
```

```text
Input: grid = [[0,2]]
Output: 0    (no fresh oranges)
```

## Constraints

- `1 <= m, n <= 10`
- `grid[i][j]` is `0`, `1`, or `2`.

## Approach

**Multi-source BFS.** All initially rotten oranges spread simultaneously, so seed the queue with **every** rotten orange at minute 0 and expand level by level; the number of BFS levels is the elapsed minutes.

**Setup:** scan once — push every rotten orange into the queue and count fresh oranges. If there are no fresh oranges, return 0 immediately.

**BFS by minute:** process the queue in level order (snapshot `len(queue)`). Each level is one minute. For every rotten orange, rot any fresh neighbor, decrement the fresh count, and enqueue it for the next level. Increment the minute counter per level that rots something.

At the end, if any fresh remain (`fresh > 0`) they were unreachable → return `-1`. Otherwise return the minute counter.

Starting all rotten oranges together naturally computes the time for the **last** orange to rot, because BFS explores in order of distance (minutes) from the nearest source.

**Complexity**

- Time: `O(m · n)`
- Space: `O(m · n)`

## Python solution

```python
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
            for _ in range(len(queue)):       # one minute's worth
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))

        return minutes if fresh == 0 else -1
```

## unittest test cases

```python
import unittest


class TestOrangesRotting(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]), 4)

    def test_example_2_impossible(self):
        self.assertEqual(self.sol.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]), -1)

    def test_example_3_no_fresh(self):
        self.assertEqual(self.sol.orangesRotting([[0, 2]]), 0)

    def test_single_fresh_no_rotten(self):
        self.assertEqual(self.sol.orangesRotting([[1]]), -1)

    def test_column_spread(self):
        self.assertEqual(self.sol.orangesRotting([[2], [1], [1], [1]]), 3)
```

## Interview tips

- **Multi-source BFS**: enqueue all rotten oranges first so they spread in parallel; a single-source BFS per orange would be wrong and slower.
- Track the fresh count and decrement as you rot; the final `fresh > 0` check detects the impossible (`-1`) case.
- Process the queue one **level** at a time (snapshot `len(queue)`); each level is one minute.
- Handle "no fresh at start" up front — the answer is `0`, not the number of BFS levels.
- Empty cells (`0`) act as walls; oranges separated from all sources by `0`s or edges can never rot.
