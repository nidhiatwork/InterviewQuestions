# LeetCode #173 - Binary Search Tree Iterator

**Data structure:** Binary Search Tree  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/binary-search-tree-iterator/

## Problem

Implement `BSTIterator` for the **in-order** traversal of a BST:

- `BSTIterator(root)` — initialize; the pointer starts before the smallest element.
- `hasNext()` — `true` if a next in-order number exists.
- `next()` — advance the pointer and return the number.

The first `next()` returns the smallest element. `next()` calls are always valid.

## Examples

```text
BSTIterator it = new BSTIterator([7,3,15,null,null,9,20]);
it.next()    -> 3
it.next()    -> 7
it.hasNext() -> true
it.next()    -> 9
it.next()    -> 15
it.next()    -> 20
it.hasNext() -> false
```

## Constraints

- The number of nodes is in `[1, 10^5]`.
- `0 <= Node.val <= 10^6`
- At most `10^5` calls to `hasNext` and `next`.

**Follow-up:** `next()` and `hasNext()` in average `O(1)` time, `O(h)` memory.

## Approach

Use a **stack** holding the path of "pending" nodes along the left spine — the iterative in-order traversal paused mid-stream, giving `O(h)` memory and amortized `O(1)` per `next()`.

In-order goes as far left as possible, visits the node, then moves to its right subtree and repeats. We pause between visits by keeping unvisited ancestors on a stack.

- **Constructor:** push the entire left spine from `root`. The top is the smallest element.
- **`next()`:** pop the top (next smallest). If it has a right child, push that child and its entire left spine.
- **`hasNext()`:** whether the stack is non-empty.

Each node is pushed and popped exactly once, so `n` calls to `next()` cost `O(n)` total → amortized `O(1)`. The stack never holds more than `h` nodes.

**Complexity**

- `next()`: amortized `O(1)`
- `hasNext()`: `O(1)`
- Space: `O(h)`

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
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
        self.assertEqual(it.next(), 15)
        self.assertEqual(it.next(), 20)
        self.assertFalse(it.hasNext())

    def test_inorder_sequence(self):
        self.assertEqual(self.drain([7, 3, 15, None, None, 9, 20]), [3, 7, 9, 15, 20])

    def test_balanced_bst(self):
        self.assertEqual(self.drain([4, 2, 6, 1, 3, 5, 7]), [1, 2, 3, 4, 5, 6, 7])
```

## Interview tips

- The stack stores the unvisited ancestors plus the current left spine; its top is always the next in-order value.
- Pre-computing the full in-order list in the constructor also works (`O(1)` calls) but uses `O(n)` memory — the stack version answers the `O(h)`-memory follow-up.
- Emphasize the amortized analysis: each node is pushed/popped once, so per-call cost averages `O(1)` even though a single `next()` may push a whole spine.
- After popping a node, only its **right** subtree can hold not-yet-seen values, so push the right child's left spine.
- `hasNext()` is just "stack not empty" — no tree walking.
