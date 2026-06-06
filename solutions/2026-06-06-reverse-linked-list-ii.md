# LeetCode #92 - Reverse Linked List II

**Data structure:** Linked List  
**Difficulty:** Medium  
**URL:** https://leetcode.com/problems/reverse-linked-list-ii/

## Problem

Given the head of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes from position `left` to position `right`, and return the resulting list.

Positions are 1-indexed.

## Examples

```text
Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]
```

```text
Input: head = [5], left = 1, right = 1
Output: [5]
```

```text
Input: head = [1,2,3], left = 1, right = 2
Output: [2,1,3]
```

## Constraints

- The number of nodes in the list is `n`.
- `1 <= n <= 500`
- `-500 <= Node.val <= 500`
- `1 <= left <= right <= n`

## Approach

Use a dummy node before the list so the same pointer logic works even when the reversal starts at the head.

1. Move `prev` to the node immediately before position `left`.
2. Set `cur = prev.next`; this node becomes the tail of the reversed segment.
3. Repeatedly remove the node after `cur` and insert it immediately after `prev`.
4. After `right - left` moves, the target window is reversed in place.

The important trick is that `cur` stays fixed while nodes after it are moved to the front of the sublist.

**Complexity**

- Time: `O(n)`
- Space: `O(1)`

## Python solution

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseBetween(self, head, left, right):
        if left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next

        cur = prev.next
        for _ in range(right - left):
            move = cur.next
            cur.next = move.next
            move.next = prev.next
            prev.next = move

        return dummy.next
```

## unittest test cases

```python
import unittest


class TestReverseBetween(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def assertReverse(self, values, left, right, expected):
        head = list_to_linked(values)
        result = self.sol.reverseBetween(head, left, right)
        self.assertEqual(linked_to_list(result), expected)

    def test_example_middle_segment(self):
        self.assertReverse([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5])

    def test_single_node(self):
        self.assertReverse([5], 1, 1, [5])

    def test_reverse_from_head(self):
        self.assertReverse([1, 2, 3], 1, 2, [2, 1, 3])

    def test_reverse_entire_list(self):
        self.assertReverse([1, 2, 3, 4], 1, 4, [4, 3, 2, 1])

    def test_left_equals_right_no_change(self):
        self.assertReverse([1, 2, 3, 4], 3, 3, [1, 2, 3, 4])
```

## Interview tips

- Start by drawing a dummy node before the list.
- Name the three key pointers: `prev`, `cur`, and `move`.
- Do not swap node values; rewire links.
- Check the `left == 1` case explicitly in your explanation.
- The most common bug is advancing `cur`; in this technique, `cur` remains the segment tail.
