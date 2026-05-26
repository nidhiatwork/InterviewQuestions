"""LeetCode #199 — Binary Tree Right Side View  (Binary Tree · Medium)

URL: https://leetcode.com/problems/binary-tree-right-side-view/

Problem
-------
Given the `root` of a binary tree, imagine yourself standing on the right
side of it. Return the values of the nodes you can see ordered from top to
bottom.

In other words, for each depth level of the tree, return the value of the
rightmost node at that level.

Examples
--------
  Input:  [1,2,3,null,5,null,4]
              1            <- visible
             / \
            2   3          <- 3 visible (right child blocks 2)
             \   \
              5   4        <- 4 visible
  Output: [1, 3, 4]

  Input:  [1, null, 3]
  Output: [1, 3]

  Input:  []
  Output: []

  # Tricky: left subtree is deeper than the right subtree at level 2,
  # so the deepest visible node from the right is actually a LEFT child.
  Input:  [1, 2, 3, 4]
              1            <- visible
             / \
            2   3          <- 3 visible
           /
          4                <- 4 visible (only node at this level)
  Output: [1, 3, 4]

Constraints
-----------
  - 0 <= number of nodes <= 100
  - -100 <= Node.val <= 100

Run
---
  python 2026-05-26-binary-tree-right-side-view.py -v
"""

import unittest
from collections import deque
from typing import List, Optional


# ----------------------------- types -----------------------------

class TreeNode:
    """Standard LeetCode binary tree node."""

    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


# ----------------------------- solution skeleton -----------------------------

class Solution:
    """Right-side view of a binary tree.

    Primary method: ``rightSideView`` — level-order BFS, one value per level.
    Follow-up:      ``right_side_view_dfs`` — DFS visiting right child first.
    Implement both. Tests below exercise both and require them to agree.
    """

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        raise NotImplementedError("Implement rightSideView (BFS level-order)")

    def right_side_view_dfs(self, root: Optional[TreeNode]) -> List[int]:
        raise NotImplementedError("Implement right_side_view_dfs (DFS, right child first)")


# ----------------------------- helpers -----------------------------

def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from a LeetCode-style level-order list with
    ``None`` markers. ``[1, None, 3]`` is a root with only a right child."""
    if not values:
        return None
    root = TreeNode(values[0])
    queue: deque[TreeNode] = deque([root])
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

class TestRightSideView(unittest.TestCase):
    def setUp(self) -> None:
        self.sol = Solution()

    def test_leetcode_example_1(self) -> None:
        root = build_tree([1, 2, 3, None, 5, None, 4])
        self.assertEqual(self.sol.rightSideView(root), [1, 3, 4])

    def test_only_right_spine(self) -> None:
        root = build_tree([1, None, 3])
        self.assertEqual(self.sol.rightSideView(root), [1, 3])

    def test_empty_tree(self) -> None:
        self.assertEqual(self.sol.rightSideView(None), [])

    def test_single_node(self) -> None:
        self.assertEqual(self.sol.rightSideView(TreeNode(42)), [42])

    def test_left_only_spine_still_visible(self) -> None:
        # Pure left spine — from the right side every node is the
        # only node at its level, so every value is visible.
        root = build_tree([1, 2, None, 3, None, 4, None])
        self.assertEqual(self.sol.rightSideView(root), [1, 2, 3, 4])

    def test_left_subtree_extends_deeper(self) -> None:
        # Subtle case: at level 2 the right child is missing, so the
        # left child (4) is the rightmost visible node at that level.
        root = build_tree([1, 2, 3, 4])
        self.assertEqual(self.sol.rightSideView(root), [1, 3, 4])

    def test_negative_values(self) -> None:
        root = build_tree([-1, -2, -3, None, -5, None, -4])
        self.assertEqual(self.sol.rightSideView(root), [-1, -3, -4])

    def test_mixed_shape_no_right_at_one_level(self) -> None:
        # Level 2 has only a LEFT grandchild; from the right we still see it.
        #         1
        #        / \
        #       2   3
        #      /
        #     5
        root = build_tree([1, 2, 3, 5, None, None, None])
        self.assertEqual(self.sol.rightSideView(root), [1, 3, 5])

    def test_perfect_tree_returns_right_spine(self) -> None:
        #         1
        #        / \
        #       2   3
        #      / \ / \
        #     4  5 6  7
        root = build_tree([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(self.sol.rightSideView(root), [1, 3, 7])

    def test_bfs_and_dfs_agree_on_many_shapes(self) -> None:
        shapes: List[List[Optional[int]]] = [
            [1, 2, 3, None, 5, None, 4],
            [1, None, 3],
            [1, 2, None, 3, None, 4, None],
            [1, 2, 3, 4],
            [1, 2, 3, 5, None, None, None],
            [1, 2, 3, 4, 5, 6, 7],
            [10, 5, 15, 3, 7, 12, 20, 1],
            [],
            [99],
        ]
        for shape in shapes:
            root = build_tree(shape)
            self.assertEqual(
                self.sol.rightSideView(root),
                self.sol.right_side_view_dfs(root),
                msg=f"BFS and DFS disagreed for {shape}",
            )


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Mental model
------------
The right-side view is exactly one value per depth level: the LAST node we
see at that depth from a left-to-right level scan. There is no
overlapping-subproblem structure here — every node is touched once and
contributes either nothing or one value to the answer. This is a traversal
problem (BFS, or DFS with an ordering trick), NOT a DP problem.

Approach 1 — Level-order BFS (the answer to lead with)
------------------------------------------------------
Walk the tree level by level with a queue. For each level take a SNAPSHOT
of its current size (`level_size = len(queue)`) and pop exactly that many
nodes. The LAST node popped on each level is the rightmost at that depth —
append its value to the result.

    from collections import deque

    def rightSideView(root):
        if root is None:
            return []
        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            rightmost = 0
            for _ in range(level_size):
                node = queue.popleft()
                rightmost = node.val          # overwritten until last node of level
                if node.left  is not None: queue.append(node.left)
                if node.right is not None: queue.append(node.right)
            result.append(rightmost)
        return result

Why this is clean:
- Children are enqueued left-then-right, so the very last `popleft()` of a
  level is guaranteed to be the rightmost node at that depth.
- One result entry per level, no `Optional` bookkeeping, no `None` checks
  inside the loop other than the children themselves.

Approach 2 — DFS, right child first
-----------------------------------
Recurse with `(node, depth)`, visiting the RIGHT child before the LEFT.
The first time we reach a given `depth`, that node IS the rightmost visible
one at that level. Detect "first time" by comparing `depth` to
`len(result)`:

    def right_side_view_dfs(root):
        result = []

        def dfs(node, depth):
            if node is None:
                return
            if depth == len(result):
                result.append(node.val)
            dfs(node.right, depth + 1)
            dfs(node.left,  depth + 1)

        dfs(root, 0)
        return result

The right-first ordering is what makes this correct on the "left subtree
deeper than right" case ([1,2,3,4] -> [1,3,4]). A naive "always follow
node.right" would output [1,3] and miss node 4 entirely.

Complexity
----------
Both approaches: O(n) time, every node visited exactly once.
- BFS: O(w) extra space, where w is the max width of the tree (worst case
  ~n/2 for a complete tree, O(1) for a skewed tree).
- DFS: O(h) recursion stack, where h is the height of the tree.

Which to use:
- Deep, narrow tree (skewed)            -> BFS uses O(1) space, DFS blows the stack.
- Wide, shallow tree (balanced)         -> DFS uses O(log n) stack vs BFS O(n) queue.
- Streaming / out-of-core               -> BFS, only one level resident at a time.

Common interview follow-ups
---------------------------
1. "Left side view?"   -> Mirror: visit LEFT child first in DFS, or take the
                          FIRST node of each BFS level (peek before the loop).
2. "Bottom view?"      -> Column-indexed BFS using horizontal distance hd:
                          root has hd=0, left child hd-1, right child hd+1.
                          Last value seen per hd in BFS order is the bottom
                          view; first value seen per hd is the top view.
3. "Stream the tree from disk, can't keep it all in RAM?"
                       -> BFS: only the current level's nodes need to be
                          resident; the rest can be page-faulted in.
4. "All views together (top, bottom, left, right)?"
                       -> Single BFS pass keyed by (depth, hd) — collect
                          first/last per depth (left/right view) and first/
                          last per hd (top/bottom view) in one walk.
5. "What if duplicate values are present?"
                       -> No change. We're returning positions' values, not
                          de-duplicating; duplicates are fine.

Traps to call out before coding
-------------------------------
- Don't confuse "right side view" with "rightmost path" (i.e., always
  follow node.right). They are NOT the same — the rightmost path misses
  visible left descendants when the right subtree is shorter.
- Don't forget the empty-tree case (return []).
- Don't materialise full levels into per-level lists if you only need one
  value per level — that's wasted O(w) work.
"""
