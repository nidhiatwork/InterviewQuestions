"""LeetCode #207 — Course Schedule  (Graph · Medium)

URL: https://leetcode.com/problems/course-schedule/

Problem
-------
There are numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [a, b] indicates
that you must take course b first if you want to take course a.

Return True if you can finish all courses. Otherwise return False.

Equivalently: determine whether the directed graph induced by the prerequisite
edges (b -> a) is acyclic.

Examples
--------
  numCourses = 2, prerequisites = [[1,0]]            ->  True
  numCourses = 2, prerequisites = [[1,0],[0,1]]      ->  False
  numCourses = 4, prerequisites = [[1,0],[2,1],[3,2]] -> True
  numCourses = 3, prerequisites = [[0,1],[1,2],[2,0]] -> False (3-cycle)

Constraints
-----------
  1 <= numCourses <= 2000
  0 <= prerequisites.length <= 5000
  prerequisites[i].length == 2
  0 <= a, b < numCourses
  All [a, b] pairs are unique.

Run
---
  python 2026-05-29-course-schedule.py -v
"""

import unittest


class Solution:
    def canFinish(self, numCourses, prerequisites):
        raise NotImplementedError("Implement canFinish")


# ----------------------------- tests -----------------------------

class TestCanFinish(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1_single_edge(self):
        self.assertTrue(self.sol.canFinish(2, [[1, 0]]))

    def test_example_2_two_cycle(self):
        self.assertFalse(self.sol.canFinish(2, [[1, 0], [0, 1]]))

    def test_linear_chain(self):
        self.assertTrue(self.sol.canFinish(4, [[1, 0], [2, 1], [3, 2]]))

    def test_three_cycle(self):
        self.assertFalse(self.sol.canFinish(3, [[0, 1], [1, 2], [2, 0]]))

    def test_no_prerequisites(self):
        self.assertTrue(self.sol.canFinish(5, []))

    def test_single_course(self):
        self.assertTrue(self.sol.canFinish(1, []))

    def test_tree_shaped_dag(self):
        # 0 is a prerequisite for 1, 2, 3; no cycles.
        prereqs = [[1, 0], [2, 0], [3, 0], [4, 1], [5, 2]]
        self.assertTrue(self.sol.canFinish(6, prereqs))

    def test_self_loop(self):
        self.assertFalse(self.sol.canFinish(3, [[0, 0]]))

    def test_two_components_one_cyclic(self):
        # Courses {0,1,2} form a DAG; courses {3,4} form a cycle.
        prereqs = [[1, 0], [2, 1], [3, 4], [4, 3]]
        self.assertFalse(self.sol.canFinish(5, prereqs))

    def test_two_components_both_dag(self):
        prereqs = [[1, 0], [2, 1], [4, 3]]
        self.assertTrue(self.sol.canFinish(5, prereqs))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The problem is asking exactly one thing: is the directed graph acyclic?
Build the directed graph (edge b -> a for each prerequisite [a, b]) and then
either (1) run Kahn's algorithm (BFS topo sort) and check that you can
process all numCourses nodes, or (2) DFS with a three-color visited array
to detect a back edge.

Kahn's BFS (preferred — easier to explain, fewer recursion-depth pitfalls):
  - Compute indegree for every node.
  - Enqueue all nodes with indegree 0.
  - Pop a node, "finish" it (counter += 1), and decrement indegree of each
    neighbor. If a neighbor's indegree drops to 0, enqueue it.
  - At the end, counter == numCourses iff acyclic.

DFS three-color (white = unseen, gray = on current stack, black = done):
  - For each unvisited node, DFS. Mark gray on entry, black on exit.
  - If you ever step onto a gray node, there's a back edge -> cycle.

Kahn's is also a free topological order, which is the natural answer to the
follow-up "Course Schedule II" (LeetCode #210). Mention that in interview.

Complexity
----------
- Time:  O(V + E)   build adjacency + each edge processed once
- Space: O(V + E)   adjacency list, indegree array, queue / recursion stack

Python solution
---------------
from collections import deque

class Solution:
    def canFinish(self, numCourses, prerequisites):
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)      # edge b -> a  (take b before a)
            indeg[a] += 1

        queue = deque(i for i in range(numCourses) if indeg[i] == 0)
        finished = 0
        while queue:
            node = queue.popleft()
            finished += 1
            for nxt in adj[node]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    queue.append(nxt)
        return finished == numCourses

# DFS three-color alternative:
#
# class Solution:
#     def canFinish(self, numCourses, prerequisites):
#         adj = [[] for _ in range(numCourses)]
#         for a, b in prerequisites:
#             adj[b].append(a)
#
#         WHITE, GRAY, BLACK = 0, 1, 2
#         color = [WHITE] * numCourses
#
#         def dfs(u):
#             color[u] = GRAY
#             for v in adj[u]:
#                 if color[v] == GRAY:
#                     return False          # back edge -> cycle
#                 if color[v] == WHITE and not dfs(v):
#                     return False
#             color[u] = BLACK
#             return True
#
#         return all(color[i] != WHITE or dfs(i) for i in range(numCourses))

Interview tips
--------------
- Reframe the problem out loud: "this is cycle detection on a directed
  graph." That's the unlock; the rest is bookkeeping.
- Be careful about edge direction. The pair [a, b] means "take b before a,"
  so the edge in the graph is b -> a. Getting this backwards still passes
  some tests but breaks the topological intuition — call it out explicitly.
- Default to Kahn's for whiteboard interviews: no recursion-depth risk
  (numCourses up to 2000 is fine for Python recursion, but easy to imagine
  a tighter constraint), and it generalizes cleanly to "return one valid
  order" (#210) by collecting the pop order.
- For the DFS variant, the three-color scheme is non-negotiable. A boolean
  visited array gives false positives on a DAG with diamond shapes (a node
  visited twice is fine; a node on the current stack is the problem).
- Microsoft follow-up: "stream of new prerequisites — detect when adding
  one would create a cycle." Answer: union-find won't work (it's for
  undirected). Maintain a topo order and use online cycle detection
  (e.g., Pearce-Kelly) — mention the trade-off; don't implement unless
  asked.
"""
