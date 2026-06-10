"""
LeetCode #235 - Lowest Common Ancestor of a Binary Search Tree
(Binary Search Tree - Medium)
URL: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

Problem
-------
Given a binary search tree (BST), find the lowest common ancestor (LCA) of two
given nodes p and q in the BST.

The lowest common ancestor is defined between two nodes p and q as the lowest
node in the tree that has both p and q as descendants (where we allow a node to
be a descendant of itself).

All node values are unique, and both p and q are guaranteed to exist in the BST.

Examples
--------
1) Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
   Output: 6
   Explanation: The LCA of nodes 2 and 8 is 6.

2) Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
   Output: 2
   Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a descendant
   of itself per the LCA definition.

3) Input:  root = [2,1], p = 2, q = 1
   Output: 2

Constraints
-----------
- The number of nodes in the tree is in the range [2, 10^5].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q will exist in the BST.

Run
---
    python 2026-06-10-lowest-common-ancestor-of-a-binary-search-tree.py -v
"""

import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def lowestCommonAncestor(self, root, p, q):
        raise NotImplementedError("Implement lowestCommonAncestor")


def build_tree(values):
    """Build a binary tree from a level-order list (None = missing node)."""
    if not values or values[0] is None:
        return None
    from collections import deque

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


def find_node(root, target_val):
    """Return the TreeNode with the given value, or None."""
    if root is None:
        return None
    if root.val == target_val:
        return root
    return find_node(root.left, target_val) or find_node(root.right, target_val)


class TestLowestCommonAncestorBST(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def lca_val(self, values, p_val, q_val):
        root = build_tree(values)
        p = find_node(root, p_val)
        q = find_node(root, q_val)
        result = self.sol.lowestCommonAncestor(root, p, q)
        return result.val if result else None

    def test_example_1(self):
        values = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
        self.assertEqual(self.lca_val(values, 2, 8), 6)

    def test_example_2_ancestor_is_self(self):
        values = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
        self.assertEqual(self.lca_val(values, 2, 4), 2)

    def test_two_node_tree(self):
        self.assertEqual(self.lca_val([2, 1], 2, 1), 2)

    def test_both_in_right_subtree(self):
        values = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
        self.assertEqual(self.lca_val(values, 7, 9), 8)

    def test_split_within_left_subtree(self):
        values = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
        self.assertEqual(self.lca_val(values, 0, 5), 2)

    def test_adjacent_inner_nodes(self):
        values = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
        self.assertEqual(self.lca_val(values, 3, 5), 4)

    def test_root_is_one_of_targets(self):
        values = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
        self.assertEqual(self.lca_val(values, 6, 9), 6)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Use the BST ordering instead of searching the whole tree.

In a BST, everything in the left subtree is smaller than the node and everything
in the right subtree is larger. So starting from the root, compare both target
values against the current node:

- If BOTH p and q are greater than the current node, the LCA must be in the
  right subtree -> move right.
- If BOTH p and q are smaller than the current node, the LCA must be in the
  left subtree -> move left.
- Otherwise the values split here (one is <= current and the other is >=, or one
  of them equals the current node). The current node is the lowest node whose
  subtree contains both, so it is the LCA -> return it.

Because we only ever walk down one branch, this is O(h) without recursion.

Complexity
----------
- Time:  O(h), where h is the tree height (O(log n) balanced, O(n) skewed).
- Space: O(1) for the iterative version (no recursion stack).

Python solution
---------------
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        node = root
        while node:
            if p.val > node.val and q.val > node.val:
                node = node.right
            elif p.val < node.val and q.val < node.val:
                node = node.left
            else:
                return node
        return None

Interview tips
--------------
- Emphasize that the BST property removes the need for a full tree search; you
  never look at both children of the same node.
- The split point - where one target is on each side (or equals the node) - is
  the LCA.
- The iterative form uses O(1) extra space; a recursive form is equally valid
  but uses O(h) stack.
- Contrast with #236 (general binary tree), which needs a full O(n) DFS because
  there is no ordering to exploit.
- Both p and q are guaranteed to exist, so you do not need existence checks; if
  that guarantee were removed, you would verify both nodes are present first.
"""
