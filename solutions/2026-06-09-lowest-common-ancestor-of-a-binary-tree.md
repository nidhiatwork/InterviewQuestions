# LeetCode #236 - Lowest Common Ancestor of a Binary Tree

**Data structure:** Binary Tree  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

## Problem

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes `p` and `q`.

The lowest common ancestor of `p` and `q` is the lowest node in the tree that has both `p` and `q` as descendants — and a node is allowed to be a descendant of itself.

All node values are unique, and both `p` and `q` are guaranteed to exist in the tree.

## Examples

```text
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
```

```text
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5   (a node can be a descendant of itself)
```

```text
Input: root = [1,2], p = 1, q = 2
Output: 1
```

## Constraints

- The number of nodes is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`, and both `p` and `q` exist in the tree.

## Approach

Do a single depth-first search and let every call report what it found below it.

For the current node:

1. If it is `None`, return `None`.
2. If it **is** `p` or `q`, return that node — a node can be its own ancestor, so we stop descending here.
3. Otherwise recurse into both children:
   - `left` = result from the left subtree
   - `right` = result from the right subtree

Then combine:

- If **both** `left` and `right` are non-`None`, the two targets were found in different subtrees, so the current node is the LCA.
- If only one side is non-`None`, bubble that result up.

The first node where the two searches meet from opposite sides is the answer.

**Complexity**

- Time: `O(n)` — each node visited once
- Space: `O(h)` — recursion stack (`O(n)` worst case for a skewed tree, `O(log n)` if balanced)

## Python solution

```python
class Solution:
    def lowestCommonAncestor(self, root, p, q):
        if root is None or root is p or root is q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root
        return left if left else right
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


def find_node(root, target_val):
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

    def test_nodes_in_opposite_subtrees(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 7, 8), 3)

    def test_root_is_one_of_targets(self):
        values = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
        self.assertEqual(self.lca_val(values, 3, 8), 3)
```

## Interview tips

- State the invariant: each call returns a target it found, or the LCA once both targets are found below.
- The "split point" — where the left and right results are both non-`None` — is the LCA.
- Compare nodes by identity (`is`), not by value, so the logic survives if the unique-values guarantee is relaxed.
- The base case `root is p or root is q` cleanly handles the "a node is its own ancestor" rule.
- For the BST variant (#235) you can do `O(h)` using value comparisons to walk down without recursion.
- With parent pointers, collect ancestors of `p` in a set and walk up from `q` until a match.
