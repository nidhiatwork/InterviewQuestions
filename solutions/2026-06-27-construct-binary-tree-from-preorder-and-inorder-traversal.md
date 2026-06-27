# LeetCode #105 - Construct Binary Tree from Preorder and Inorder Traversal

**Data structure:** Binary Tree  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

## Problem

Given two integer arrays `preorder` and `inorder` — the preorder and inorder traversals of the same binary tree — construct and return the tree.

## Examples

```text
Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

```text
Input: preorder = [-1], inorder = [-1]
Output: [-1]
```

## Constraints

- `1 <= preorder.length <= 3000`, `inorder.length == preorder.length`
- `-3000 <= values <= 3000`, all values unique.
- `preorder`/`inorder` are valid traversals of the same tree.

## Approach

The first element of `preorder` is always the root. Find it in `inorder`: everything to its **left** is the left subtree, everything to its **right** is the right subtree. Recurse on those slices.

Two tricks turn the naive `O(n^2)` into `O(n)`:

1. Build a hash map `value -> index` for `inorder`, so locating the root is `O(1)`.
2. Walk `preorder` with a single moving pointer (shared index) instead of slicing, passing `inorder` bounds `(left, right)` to delimit the current subtree.

**Algorithm:**

- Keep a global `pre_idx` into `preorder`, starting at 0.
- `helper(left, right)` builds the subtree spanning `inorder[left..right]`:
  - if `left > right`: return `None`.
  - `root_val = preorder[pre_idx]`; advance `pre_idx`.
  - `mid = index[root_val]`.
  - Recurse **left first** (`helper(left, mid - 1)`), then **right** (`helper(mid + 1, right)`) — matching preorder's root → left → right shape.

**Complexity**

- Time: `O(n)` — each node created once with `O(1)` root lookup
- Space: `O(n)` index map + `O(h)` recursion stack

## Python solution

```python
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
```

## unittest test cases

```python
import unittest


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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

    def test_left_skewed(self):
        self.assertReconstructs([3, 2, 1], [1, 2, 3])

    def test_balanced(self):
        self.assertReconstructs([4, 2, 1, 3, 6, 5, 7], [1, 2, 3, 4, 5, 6, 7])
```

## Interview tips

- The crux: preorder gives the root order; inorder splits each root into left/right subtrees. You need **both** to reconstruct uniquely.
- Use a `value -> index` map on inorder so root lookup is `O(1)` — this is what makes it `O(n)` not `O(n^2)`.
- Advance the preorder pointer in the **same order** you recurse (left before right), matching preorder's root-left-right shape — swapping is the classic bug.
- Unique values are required for the index map; duplicates would make reconstruction ambiguous.
- A postorder + inorder variant works similarly, but you consume postorder from the **end** and recurse **right before left**.
