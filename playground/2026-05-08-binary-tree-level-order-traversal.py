"""LeetCode #102 — Binary Tree Level Order Traversal  (Binary Tree · Medium)

URL: https://leetcode.com/problems/binary-tree-level-order-traversal/

Problem
-------
Given the root of a binary tree, return the level-order traversal of its nodes'
values (from left to right, level by level).

Examples
--------
  root = [3,9,20,null,null,15,7]  ->  [[3],[9,20],[15,7]]
  root = [1]                      ->  [[1]]
  root = []                       ->  []

Constraints
-----------
  Number of nodes in [0, 2000];  -1000 <= Node.val <= 1000.

Run
---
  python 2026-05-08-binary-tree-level-order-traversal.py -v
"""

from collections import deque
import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root):
        raise NotImplementedError("Implement levelOrder")


# ----------------------------- helpers -----------------------------

def build_tree(values):
    """Build a binary tree from a level-order list with None for missing children."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


# ----------------------------- tests -----------------------------

class TestLevelOrder(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        root = build_tree([3, 9, 20, None, None, 15, 7])
        self.assertEqual(self.solution.levelOrder(root), [[3], [9, 20], [15, 7]])

    def test_single_node(self):
        root = build_tree([1])
        self.assertEqual(self.solution.levelOrder(root), [[1]])

    def test_empty_tree(self):
        self.assertEqual(self.solution.levelOrder(None), [])

    def test_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
        self.assertEqual(self.solution.levelOrder(root), [[1], [2], [3], [4]])

    def test_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        self.assertEqual(self.solution.levelOrder(root), [[1], [2], [3]])

    def test_complete_tree(self):
        root = build_tree([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(self.solution.levelOrder(root), [[1], [2, 3], [4, 5, 6, 7]])

    def test_negative_values(self):
        root = build_tree([-1, -2, -3, None, -4])
        self.assertEqual(self.solution.levelOrder(root), [[-1], [-2, -3], [-4]])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
BFS with a queue, level-sized batches. Each outer iteration captures
`level_size = len(queue)` at the start, then dequeues exactly that many nodes
(the current level), enqueueing their children for the next level.

Complexity
----------
- Time:  O(n)            (each node enqueued and dequeued once)
- Space: O(w)            (max tree width; worst case n/2 -> O(n))

Python solution
---------------
from collections import deque

class Solution:
    def levelOrder(self, root):
        if root is None:
            return []
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            result.append(level)
        return result

Interview tips
--------------
- Level boundary is the key insight: capture `len(queue)` at iteration start.
  Without that you'd need a sentinel value or (node, depth) tuples.
- Empty-tree branch first (`if root is None: return []`) — forgetting throws
  on popleft from an empty queue.
- Why deque? popleft() is O(1); list.pop(0) is O(n). Flag the guarantee.
- DFS alternative: pass depth, append to result[depth]. BFS is O(w), DFS is
  O(h); pick based on tree shape.
- Variations to expect: zigzag (LC 103), bottom-up (LC 107), right-side view
  (LC 199) — all reuse the same level-boundary skeleton.
"""
