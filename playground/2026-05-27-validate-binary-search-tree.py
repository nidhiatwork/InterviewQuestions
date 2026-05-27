"""LeetCode #98 — Validate Binary Search Tree  (Binary Search Tree · Medium)

URL: https://leetcode.com/problems/validate-binary-search-tree/

Problem
-------
Given the root of a binary tree, determine if it is a valid binary search
tree (BST). A valid BST is defined as follows:
  - The left subtree of a node contains only nodes with keys strictly less
    than the node's key.
  - The right subtree of a node contains only nodes with keys strictly
    greater than the node's key.
  - Both the left and right subtrees must themselves be BSTs.

Examples
--------
  root = [2,1,3]                 ->  True
  root = [5,1,4,null,null,3,6]   ->  False   (4's left child 3 < root 5)
  root = [2,2,2]                 ->  False   (duplicates not allowed — strict)
  root = [10,5,15,null,null,6,20] -> False   (6 sits in 15's left subtree but 6 < 10)

Constraints
-----------
  Number of nodes in the tree is in the range [1, 10^4].
  -2^31 <= Node.val <= 2^31 - 1

Run
---
  python 2026-05-27-validate-binary-search-tree.py -v
"""

import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root):
        raise NotImplementedError("Implement isValidBST")


# ----------------------------- helpers -----------------------------

def build_tree(values):
    """Build a tree from a LeetCode-style level-order list with None for gaps."""
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
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

class TestIsValidBST(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1_simple_valid(self):
        root = build_tree([2, 1, 3])
        self.assertTrue(self.sol.isValidBST(root))

    def test_example_2_grandchild_violation(self):
        root = build_tree([5, 1, 4, None, None, 3, 6])
        self.assertFalse(self.sol.isValidBST(root))

    def test_single_node(self):
        self.assertTrue(self.sol.isValidBST(TreeNode(42)))

    def test_duplicates_are_invalid(self):
        root = build_tree([2, 2, 2])
        self.assertFalse(self.sol.isValidBST(root))

    def test_deep_left_violation(self):
        root = build_tree([10, 5, 15, None, None, 6, 20])
        self.assertFalse(self.sol.isValidBST(root))

    def test_left_skewed_valid(self):
        root = TreeNode(4, TreeNode(3, TreeNode(2, TreeNode(1))))
        self.assertTrue(self.sol.isValidBST(root))

    def test_right_skewed_valid(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
        self.assertTrue(self.sol.isValidBST(root))

    def test_int_min_root_with_left_violation(self):
        # If we used a naive parent-only check, INT_MIN as the only node would pass
        # but a left child equal to INT_MIN should fail (BST must be strict).
        root = TreeNode(-2**31, TreeNode(-2**31), None)
        self.assertFalse(self.sol.isValidBST(root))

    def test_extreme_values_valid(self):
        root = TreeNode(0, TreeNode(-2**31), TreeNode(2**31 - 1))
        self.assertTrue(self.sol.isValidBST(root))

    def test_inorder_looks_sorted_but_structure_broken(self):
        # In-order yields [1, 2, 3] which is sorted, but the right child of 3 is 2,
        # which means structurally invalid. Make sure the check is structural,
        # not just "in-order sorted ascending."
        # Tree:  3
        #       / \
        #      2   ?  (no right)
        #     /
        #    1
        # Add a tricky case: 3 has left=2 (ok) and right=1 (violates).
        root = TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(1))
        self.assertFalse(self.sol.isValidBST(root))


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The classic trap is to validate each node against only its immediate parent.
That misses violations where a descendant lives in the wrong global window
(see #5, "deep left violation": the node 6 is fine vs. its parent 15, but
must also be > 10 because it sits in 10's right subtree).

Carry a (lo, hi) open interval down the recursion. At every node:
  - node.val must satisfy  lo < node.val < hi  (strict on both sides).
  - Recurse left with hi = node.val.
  - Recurse right with lo = node.val.

Use Python's None as +/- infinity sentinels (or math.inf) so you don't have
to hardcode INT_MIN / INT_MAX — which also dodges the edge case where the
root itself is INT_MIN with an equal child.

Iterative alternative: in-order traversal with a `prev` pointer; require
prev.val < node.val at every pop. Same O(n) / O(h), different control flow.

Complexity
----------
- Time:  O(n)   every node is visited once
- Space: O(h)   recursion stack; h = tree height (O(log n) balanced, O(n) skewed)

Python solution
---------------
class Solution:
    def isValidBST(self, root):
        def walk(node, lo, hi):
            if node is None:
                return True
            if (lo is not None and node.val <= lo) or (hi is not None and node.val >= hi):
                return False
            return walk(node.left, lo, node.val) and walk(node.right, node.val, hi)

        return walk(root, None, None)

# Iterative in-order alternative (often easier to discuss in an interview):
#
# class Solution:
#     def isValidBST(self, root):
#         stack = []
#         prev = None
#         node = root
#         while node is not None or stack:
#             while node is not None:
#                 stack.append(node)
#                 node = node.left
#             node = stack.pop()
#             if prev is not None and node.val <= prev.val:
#                 return False
#             prev = node
#             node = node.right
#         return True

Interview tips
--------------
- Open with the failure mode of the naive parent-only check (the classic trap).
  Showing you know *why* it's wrong is half the signal.
- Strict inequality matters: duplicates are NOT allowed in a BST by the
  standard definition. Confirm this assumption with the interviewer up front.
- Use None / math.inf as bounds — avoids the INT_MIN / INT_MAX corner case
  where a root equal to the sentinel breaks a hardcoded version.
- Mention the iterative in-order variant as a follow-up; it generalizes to
  "is the in-order traversal strictly increasing?" which is a clean mental
  model for the whole problem.
- Microsoft follow-up: "recover" a BST where exactly two nodes are swapped
  (LeetCode #99) — same in-order skeleton, different bookkeeping.
"""
