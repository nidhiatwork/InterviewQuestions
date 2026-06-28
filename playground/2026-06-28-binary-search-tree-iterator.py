"""
LeetCode #173 - Binary Search Tree Iterator  (Binary Search Tree - Medium)
URL: https://leetcode.com/problems/binary-search-tree-iterator/

Problem
-------
Implement the BSTIterator class that represents an iterator over the in-order
traversal of a binary search tree (BST):

  - BSTIterator(TreeNode root) Initializes an object of the BSTIterator class. The
    root of the BST is given as part of the constructor. The pointer should be
    initialized to a non-existent number smaller than any element in the BST.
  - boolean hasNext() Returns true if there exists a number in the traversal to
    the right of the pointer, otherwise returns false.
  - int next() Moves the pointer to the right, then returns the number at the
    pointer.

Notice that by initializing the pointer to a non-existent smallest number, the
first call to next() will return the smallest element in the BST.

You may assume that next() calls will always be valid. That is, there will be at
least a next number in the in-order traversal when next() is called.

Examples
--------
Input
  ["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
  [[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
Output
  [null, 3, 7, true, 9, true, 15, true, 20, false]

Explanation
  BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
  bSTIterator.next();    // return 3
  bSTIterator.next();    // return 7
  bSTIterator.hasNext(); // return True
  bSTIterator.next();    // return 9
  bSTIterator.hasNext(); // return True
  bSTIterator.next();    // return 15
  bSTIterator.hasNext(); // return True
  bSTIterator.next();    // return 20
  bSTIterator.hasNext(); // return False

Constraints
-----------
- The number of nodes in the tree is in the range [1, 10^5].
- 0 <= Node.val <= 10^6
- At most 10^5 calls will be made to hasNext, and next.

Follow-up
---------
Could you implement next() and hasNext() to run in average O(1) time and use
O(h) memory, where h is the height of the tree?

Run
---
    python 2026-06-28-binary-search-tree-iterator.py -v
"""

import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    def __init__(self, root):
        raise NotImplementedError("Implement BSTIterator.__init__")

    def next(self):
        raise NotImplementedError("Implement next")

    def hasNext(self):
        raise NotImplementedError("Implement hasNext")


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


class TestBSTIterator(unittest.TestCase):
    def drain(self, values):
        """Return the full in-order sequence produced by the iterator."""
        it = BSTIterator(build_tree(values))
        result = []
        while it.hasNext():
            result.append(it.next())
        return result

    def test_example(self):
        it = BSTIterator(build_tree([7, 3, 15, None, None, 9, 20]))
        self.assertEqual(it.next(), 3)
        self.assertEqual(it.next(), 7)
        self.assertTrue(it.hasNext())
        self.assertEqual(it.next(), 9)
        self.assertTrue(it.hasNext())
        self.assertEqual(it.next(), 15)
        self.assertTrue(it.hasNext())
        self.assertEqual(it.next(), 20)
        self.assertFalse(it.hasNext())

    def test_single_node(self):
        it = BSTIterator(build_tree([5]))
        self.assertTrue(it.hasNext())
        self.assertEqual(it.next(), 5)
        self.assertFalse(it.hasNext())

    def test_inorder_sequence(self):
        self.assertEqual(
            self.drain([7, 3, 15, None, None, 9, 20]), [3, 7, 9, 15, 20]
        )

    def test_left_skewed(self):
        # 5 -> 4 -> 3 -> 2 -> 1 all on left
        values = [5, 4, None, 3, None, 2, None, 1]
        self.assertEqual(self.drain(values), [1, 2, 3, 4, 5])

    def test_right_skewed(self):
        values = [1, None, 2, None, 3, None, 4, None, 5]
        self.assertEqual(self.drain(values), [1, 2, 3, 4, 5])

    def test_balanced_bst(self):
        values = [4, 2, 6, 1, 3, 5, 7]
        self.assertEqual(self.drain(values), [1, 2, 3, 4, 5, 6, 7])

    def test_hasnext_false_at_end(self):
        it = BSTIterator(build_tree([2, 1, 3]))
        self.assertEqual([it.next(), it.next(), it.next()], [1, 2, 3])
        self.assertFalse(it.hasNext())


if __name__ == "__main__":
    unittest.main()


# ============================================================================
# REFERENCE SOLUTION & NOTES  - peek only if stuck
# ============================================================================

REFERENCE = """
Approach
--------
Use a stack that holds the path of "pending" nodes along the left spine. This is
the iterative in-order traversal paused mid-stream, giving O(h) memory and
amortized O(1) per next().

Idea: an in-order traversal goes as far left as possible, visits the node, then
moves to its right subtree and repeats. We can pause this process between visits
by keeping the unvisited ancestors on a stack.

  - Constructor: push the entire left spine from root (root, root.left,
    root.left.left, ...). The top of the stack is therefore the smallest element.
  - next(): pop the top node (the next smallest). Before returning its value, if
    it has a right child, push the right child and that child's entire left spine.
    This stages the next in-order elements.
  - hasNext(): simply whether the stack is non-empty.

Each node is pushed and popped exactly once across the whole iteration, so n
calls to next() cost O(n) total -> amortized O(1) each. The stack never holds more
than h nodes (one per level of the current left spine), giving O(h) memory.

Complexity
----------
- next():    amortized O(1) (O(n) total work over n calls).
- hasNext(): O(1).
- Space:     O(h) for the stack.

Python solution
---------------
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()       # next smallest
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self):
        return len(self.stack) > 0

Interview tips
--------------
- The stack stores the unvisited ancestors plus the current left spine; its top
  is always the next in-order value.
- Pre-computing the full in-order list in the constructor also works and makes
  next()/hasNext() trivially O(1), but it uses O(n) memory - the stack version is
  what answers the O(h)-memory follow-up.
- Emphasize the amortized analysis: each node is pushed/popped once, so the per
  -call cost averages O(1) even though a single next() may push a whole spine.
- After popping a node, only its RIGHT subtree can contain not-yet-seen smaller
  -than-ancestors values, so you push the right child's left spine.
- hasNext() is just "stack not empty" - no tree walking needed.
"""
