"""LeetCode #230 — Kth Smallest Element in a BST  (Binary Search Tree · Medium)

URL: https://leetcode.com/problems/kth-smallest-element-in-a-bst/

Problem
-------
Given the root of a binary search tree and an integer k, return the k-th
smallest value (1-indexed) among all the nodes' values.

Examples
--------
  root = [3,1,4,null,2], k = 1                ->  1
  root = [5,3,6,2,4,null,null,1], k = 3       ->  3

Constraints
-----------
  1 <= k <= n <= 10^4
  0 <= Node.val <= 10^4

Run
---
  python 2026-05-11-kth-smallest-element-in-a-bst.py -v
"""

import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root, k):
        raise NotImplementedError("Implement kthSmallest")


# ----------------------------- helpers -----------------------------

def build_tree(values):
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

class TestKthSmallest(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        root = build_tree([3, 1, 4, None, 2])
        self.assertEqual(self.sol.kthSmallest(root, 1), 1)

    def test_example_2(self):
        root = build_tree([5, 3, 6, 2, 4, None, None, 1])
        self.assertEqual(self.sol.kthSmallest(root, 3), 3)

    def test_single_node(self):
        root = TreeNode(7)
        self.assertEqual(self.sol.kthSmallest(root, 1), 7)

    def test_kth_is_root(self):
        root = build_tree([5, 3, 6, 2, 4, None, None, 1])
        self.assertEqual(self.sol.kthSmallest(root, 4), 5)

    def test_kth_is_largest(self):
        root = build_tree([5, 3, 6, 2, 4, None, None, 1])
        self.assertEqual(self.sol.kthSmallest(root, 6), 6)

    def test_right_skewed(self):
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4))))
        self.assertEqual(self.sol.kthSmallest(root, 4), 4)

    def test_left_skewed(self):
        root = TreeNode(4, TreeNode(3, TreeNode(2, TreeNode(1))))
        self.assertEqual(self.sol.kthSmallest(root, 1), 1)


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  — peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
In-order traversal of a BST yields nodes in sorted ascending order. The k-th
element of that in-order walk is the answer.

Use iterative in-order with an explicit stack so you can stop at exactly the
k-th pop instead of walking the whole tree.

Complexity
----------
- Time:  O(h + k)     average; worst-case O(n + k) for a skewed BST
- Space: O(h)         (the stack)

Python solution
---------------
class Solution:
    def kthSmallest(self, root, k):
        stack = []
        node = root
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            k -= 1
            if k == 0:
                return node.val
            node = node.right

Interview tips
--------------
- Lead with the BST property: in-order = sorted. That's the unlock.
- Prefer iterative stack-based traversal — lets you stop at the k-th pop.
- Follow-up Microsoft almost always asks: "What if the BST is modified often
  and you need many kthSmallest calls?" Augment nodes with a `leftCount`
  field (size of left subtree); each query becomes O(h).
"""
