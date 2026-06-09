"""
LeetCode #236 - Lowest Common Ancestor of a Binary Tree  (Binary Tree - Medium)
URL: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

Problem
-------
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p
and q in the tree.

The lowest common ancestor is defined between two nodes p and q as the lowest
node in the tree that has both p and q as descendants (where we allow a node to
be a descendant of itself).

All node values are unique, and both p and q are guaranteed to exist in the
tree.

Examples
--------
1) Input:  root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
   Output: 3
   Explanation: The LCA of nodes 5 and 1 is 3.

2) Input:  root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
   Output: 5
   Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant
   of itself.

3) Input:  root = [1,2], p = 1, q = 2
   Output: 1

Constraints
-----------
- The number of nodes in the tree is in the range [2, 10^5].
- -10^9 <= Node.val <= 10^9
- All Node.val are unique.
- p != q
- p and q will exist in the tree.

Run
---
    python 2026-06-09-lowest-common-ancestor-of-a-binary-tree.py -v
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


class TestLowestCommonAncestor(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def lca_val(self, values, p_val, q_val):
        root = build_tree(values)
        p = find_node(root, p_val)
        q = find_node(root, q_val)
        result = self.sol.lowestCommonAncestor(root, p, q)
        return result.val if result else None

    def test_example_1(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 5, 1), 3)

    def test_example_2_ancestor_is_self(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 5, 4), 5)

    def test_two_node_tree(self):
        self.assertEqual(self.lca_val([1, 2], 1, 2), 1)

    def test_deep_left_chain(self):
        # 1 -> 2 -> 3 -> 4 all on left spine
        values = [1, 2, None, 3, None, 4]
        self.assertEqual(self.lca_val(values, 3, 4), 3)

    def test_nodes_in_opposite_subtrees(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 7, 8), 3)

    def test_lca_within_left_subtree(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 6, 4), 5)

    def test_root_is_one_of_targets(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 3, 8), 3)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Recurse from the root and let each call report whether the subtree below it
contains p, q, or the answer.

For the current node:
- If it is None, return None (nothing found here).
- If it equals p or q, return the node itself. A node can be its own ancestor,
  so we stop descending once we hit a target.
- Otherwise, recurse into both children:
    * left  = search the left subtree
    * right = search the right subtree
  Then:
    * If BOTH left and right come back non-None, p and q were found in
      different subtrees, so the current node is their lowest common ancestor.
    * If only one side is non-None, the answer (or a target) lives entirely on
      that side, so bubble it up.

The first node where the two search results meet from opposite sides is the LCA.
A single DFS visits every node once.

Complexity
----------
- Time:  O(n), each node is visited once.
- Space: O(h), recursion stack where h is the tree height (O(n) worst case for
  a skewed tree, O(log n) for a balanced tree).

Python solution
---------------
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root
        return left if left else right

Interview tips
--------------
- State the key invariant: each call returns a target node it found, or the LCA
  if both targets were found below.
- The "split point" - where left and right are both non-None - is the LCA.
- Compare nodes by identity (`is`), not by value, so the logic is robust even if
  the interviewer relaxes the unique-values guarantee.
- Mention the base case `root is p or root is q` handles the "a node is its own
  ancestor" rule cleanly.
- If asked for the BST variant (#235), you can do better: walk down using value
  comparisons in O(h) without recursion.
- If parent pointers were available, an alternative is to collect ancestors of p
  in a set and walk up from q until a match.
"""
