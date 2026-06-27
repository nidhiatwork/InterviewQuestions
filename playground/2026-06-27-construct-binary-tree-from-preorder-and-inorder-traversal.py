"""
LeetCode #105 - Construct Binary Tree from Preorder and Inorder Traversal
(Binary Tree - Medium)
URL: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Problem
-------
Given two integer arrays preorder and inorder where preorder is the preorder
traversal of a binary tree and inorder is the inorder traversal of the same tree,
construct and return the binary tree.

Examples
--------
1) Input:  preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
   Output: [3,9,20,null,null,15,7]

2) Input:  preorder = [-1], inorder = [-1]
   Output: [-1]

Constraints
-----------
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values.
- Each value of inorder also appears in preorder.
- preorder is guaranteed to be the preorder traversal of the tree.
- inorder is guaranteed to be the inorder traversal of the tree.

Run
---
    python 2026-06-27-construct-binary-tree-from-preorder-and-inorder-traversal.py -v
"""

import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, preorder, inorder):
        raise NotImplementedError("Implement buildTree")


def preorder_traversal(root):
    if root is None:
        return []
    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)


def inorder_traversal(root):
    if root is None:
        return []
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)


class TestBuildTree(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertReconstructs(self, preorder, inorder):
        root = self.sol.buildTree(preorder, inorder)
        self.assertEqual(preorder_traversal(root), preorder)
        self.assertEqual(inorder_traversal(root), inorder)

    def test_example_1(self):
        self.assertReconstructs([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])

    def test_single_node(self):
        root = self.sol.buildTree([-1], [-1])
        self.assertEqual(root.val, -1)
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)

    def test_left_skewed(self):
        # tree: 3 -> 2 -> 1 all on the left
        self.assertReconstructs([3, 2, 1], [1, 2, 3])

    def test_right_skewed(self):
        # tree: 1 -> 2 -> 3 all on the right
        self.assertReconstructs([1, 2, 3], [1, 2, 3])

    def test_balanced(self):
        self.assertReconstructs([4, 2, 1, 3, 6, 5, 7], [1, 2, 3, 4, 5, 6, 7])

    def test_root_structure_example(self):
        root = self.sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
        self.assertEqual(root.val, 3)
        self.assertEqual(root.left.val, 9)
        self.assertEqual(root.right.val, 20)
        self.assertEqual(root.right.left.val, 15)
        self.assertEqual(root.right.right.val, 7)

    def test_negative_and_positive(self):
        self.assertReconstructs([0, -3, -10, 9, 5], [-10, -3, 9, 0, 5])


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
The first element of preorder is always the root. Find that root in inorder: every
value to its LEFT in inorder is the left subtree, everything to its RIGHT is the
right subtree. Recurse on those slices.

Two efficiency tricks turn the naive O(n^2) into O(n):
  1. Build a hash map value -> index for inorder, so locating the root is O(1)
     instead of a linear scan.
  2. Walk preorder with a single moving pointer (a shared index) instead of
     slicing the list, and pass inorder bounds (left, right) to delimit the
     current subtree.

Algorithm:
  - Keep a global position `pre_idx` into preorder, starting at 0.
  - helper(left, right) builds the subtree spanning inorder[left..right]:
      * if left > right: return None (empty subtree).
      * root_val = preorder[pre_idx]; advance pre_idx.
      * mid = index_in_inorder[root_val].
      * Recurse LEFT first (helper(left, mid - 1)), then RIGHT
        (helper(mid + 1, right)) - this order matches how preorder lists root,
        then entire left subtree, then entire right subtree.
      * Return the constructed node.

Because preorder visits root -> left subtree -> right subtree, advancing pre_idx
in that exact recursion order consumes the right roots at the right times.

Complexity
----------
- Time:  O(n), each node created once with O(1) root lookup.
- Space: O(n) for the index map plus O(h) recursion stack.

Python solution
---------------
class Solution:
    def buildTree(self, preorder, inorder):
        index = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0

        def helper(left, right):
            if left > right:
                return None
            root_val = preorder[self.pre_idx]
            self.pre_idx += 1
            root = TreeNode(root_val)
            mid = index[root_val]
            root.left = helper(left, mid - 1)     # build left subtree first
            root.right = helper(mid + 1, right)   # then right subtree
            return root

        return helper(0, len(inorder) - 1)

Interview tips
--------------
- The crux: preorder gives you the root order; inorder splits each root into left
  and right subtrees. You need BOTH to reconstruct uniquely.
- Use a value->index map on inorder so root lookup is O(1); this is what makes it
  O(n) rather than O(n^2).
- Advance the preorder pointer in the SAME order you recurse (left before right),
  matching preorder's root-left-right shape - swapping the order is the classic
  bug.
- Unique values are required for the index map; mention that duplicates would make
  the reconstruction ambiguous.
- A postorder + inorder variant works similarly, but you consume postorder from
  the END and recurse RIGHT before LEFT.
"""
